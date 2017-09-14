from flask import request, jsonify, abort, current_app
from app.models import Business, Status, Vendor, get_or_create
from app.schemas import *
from sqlalchemy import exc
import logging

logger = logging.getLogger(__name__)


def businesses():
    if request.method == "POST":
        json_data = request.get_json()
        if not json_data:
            return jsonify({'message': 'No input data provided'}), 400
        # Validate and deserialize input
        data, errors = business_schema.load(json_data)
        if errors:
            return jsonify(errors), 422

        name = json_data.get('name')
        try:
            status_name = json_data["status"]["name"]
        except KeyError:
            status_name = 'pending'
        if name:
            try:
                status = Status.query.filter_by(name=status_name).first()
                if status is None:
                    status, created = get_or_create(current_app.db, Status, name=status_name)
                    logging.info("status [%s] was created: [%s]" % (status.name, created))
                business = Business(name=name, status=status)
                business.save()
                obj = business_schema.dump(business)
                response = jsonify(obj.data)
                response.status_code = 201
            except exc.IntegrityError as e:
                current_app.db.session.rollback()
                response = jsonify({'error': 'Business [%s] already exists' % name})
                logger.error(repr(e))
                response.status_code = 400
            return response

    elif request.method == "PATCH":
        json_data = request.get_json()
        if not json_data:
            return jsonify({'message': 'No input data provided'}), 400
        # Validate and deserialize input
        data, errors = partner_schema.load(json_data)
        if errors:
            return jsonify(errors), 422
        results = []
        status_code = 404
        name = json_data.get('name')
        try:
            vendor_name = json_data["vendor"]["name"]
        except KeyError:
            vendor_name = None

        try:
            status_name = json_data["status"]["name"]
        except KeyError:
            status_name = None
        business = Business.query.filter_by(name=name).first()

        if business is None:
            message = {'name': 'Business object [%s] was not found' % repr(name)}
            results.append(message)

        if business:
            try:
                if status_name:
                    status = Status.query.filter_by(name=status_name).first()
                    if status is None:
                        status, created = get_or_create(current_app.db, Status, name=status_name)
                        logging.info("status [%s] was created: [%s]" % (status.name, created))
                    business.status = status
                if vendor_name:
                    vendor = Vendor.query.filter_by(name=vendor_name).first()
                    if vendor is None:
                        message = {'vendor': 'Vendor object [%s] was not found' % repr(vendor_name)}
                        results.append(message)
                        response = jsonify(results)
                        response.status_code = 404
                        return response
                    else:
                        current_app.db.session.add(vendor)
                        current_app.db.session.add(business)
                        business.vendors.append(vendor)
                current_app.db.session.commit()
                obj = business_schema.dump(business)
                results.append(obj.data)
                status_code = 200
            except exc.IntegrityError as e:
                current_app.db.session.rollback()
                results.append({'error': 'Relation already exists'})
                logger.error(repr(e))
                status_code = 400

        response = jsonify(results)
        response.status_code = status_code
        return response

    else:
        # GET
        businesses = Business.get_all()
        results = businesses_schema.dump(businesses)
        response = jsonify(results.data)
        response.status_code = 200
        return response


def vendors():
    if request.method == "POST":
        json_data = request.get_json()
        if not json_data:
            return jsonify({'message': 'No input data provided'}), 400
        # Validate and deserialize input
        data, errors = vendor_schema.load(json_data)
        if errors:
            return jsonify(errors), 422

        name = json_data.get('name')
        status_name = json_data.get('status').get('name')
        status = Status.query.filter_by(name=status_name).first()

        if status is None:
            status, created = get_or_create(current_app.db, Status, name=status_name)
            logging.info("status [%s] was created: [%s]" % (status.name, created))

        if name:
            try:
                vendor = Vendor(name=name, status=status)
                vendor.save()
                obj = vendor_schema.dump(vendor)
                response = jsonify(obj.data)
                response.status_code = 201
            except exc.IntegrityError as e:
                current_app.db.session.rollback()
                response = jsonify({'error': 'Vendor [%s] already exists' % name})
                logger.error(repr(e))
                response.status_code = 400
            return response

    elif request.method == "PATCH":
        json_data = request.get_json()
        if not json_data:
            return jsonify({'message': 'No input data provided'}), 400
        # Validate and deserialize input
        data, errors = vendor_schema.load(json_data)
        if errors:
            return jsonify(errors), 422

        name = json_data.get('name')
        status_name = json_data.get("status").get("name")

        vendor = Vendor.query.filter_by(name=name).first()
        if vendor is None:
            message = {'name': 'Business object [%s] was not found' % repr(name)}
            response = jsonify(message)
            response.status_code = 404
            return response

        status = Status.query.filter_by(name=status_name).first()
        if status is None:
            message = {'name': 'Status object [%s] was not found' % repr(status_name)}
            response = jsonify(message)
            response.status_code = 404
            return response
        vendor.status = status
        vendor.save()
        response = vendor_schema.jsonify(vendor)
        response.status_code = 200
        return response

    else:
        # GET
        vendors = Vendor.get_all()
        results = vendors_schema.dump(vendors)
        response = jsonify(results.data)
        response.status_code = 200
        return response


def statuses():
    if request.method == "POST":
        json_data = request.get_json()
        if not json_data:
            return jsonify({'message': 'No input data provided'}), 400
        # Validate and deserialize input
        data, errors = status_schema.load(json_data)
        if errors:
            return jsonify(errors), 422

        name = json_data.get('name')

        if name:
            try:
                status = Status(name=name)
                status.save()
                obj = status_schema.dump(status)
                response = jsonify(obj.data)
                response.status_code = 201
            except exc.IntegrityError as e:
                current_app.db.session.rollback()
                response = jsonify({'error': 'Status [%s] already exists' % name})
                logger.error(repr(e))
                response.status_code = 400
            return response
    else:
        # GET
        statuses = Status.get_all()
        results = statuses_schema.dump(statuses)
        response = jsonify(results.data)
        response.status_code = 200
        return response
