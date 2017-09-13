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
        status = json_data.get('status')
        status = Status.query.filter_by(name=status).first()
        if status is None:
            status, created = get_or_create(current_app.db, Status, name='pending')
        print("name: [%s]" % name)
        if name:
            business = Business(name=name, status=status)
            business.save()
            obj = business_schema.dump(business)
            response = jsonify(obj.data)
            response.status_code = 201
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
        vendor_name = json_data.get('vendor')
        business = Business.query.filter_by(name=name).first()
        vendor = Vendor.query.filter_by(name=vendor_name).first()

        if business is None:
            message = {'name': 'Business object [%s] was not found' % repr(name)}
            results.append(message)

        if vendor is None:
            message = {'vendor': 'Vendor object [%s] was not found' % repr(vendor_name)}
            results.append(message)

        if business and vendor:
            try:
                current_app.db.session.add(vendor)
                current_app.db.session.add(business)
                business.vendors.append(vendor)
                current_app.db.session.commit()
                obj = business_schema.dump(business)
                results.append(obj.data)
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
        name = str(request.data.get('name'))
        status = str(request.data.get('status'))
        status = Status.query.filter_by(name=status).first()
        if status is None:
            status, created = get_or_create(current_app.db, Status, name='pending')

        if name:
            vendor = Vendor(name=name, status=status)
            vendor.save()
            obj = vendor_schema.dump(vendor)
            response = jsonify(obj.data)
            response.status_code = 201
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
        name = str(request.data.get('name'))

        if name:
            status = Status(name=name)
            status.save()
            obj = status_schema.dump(status)
            response = jsonify(obj.data)
            response.status_code = 201
            return response
    else:
        # GET
        statuses = Status.get_all()
        results = statuses_schema.dump(statuses)
        response = jsonify(results.data)
        response.status_code = 200
        return response
