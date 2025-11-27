
# @main.route('/api/services')
# def get_services():
#     try:
#         services = redis_client.get('all_service')
#         if services:
#             services = json.loads(services)
#         else:
#             services = Service.query.all()
#             service_list = []
#             for service in services:
#                 service_data = {
#                     'service_id': service.service_id,
#                     'name': service.name,
#                     'base_price': service.base_price,
#                     'required_time': service.required_time,
#                     'description': service.description,
#                     'status': service.status
#                 }
#                 service_list.append(service_data)
#             redis_client.setex('all_service', 600, json.dumps(service_list))
#             services = service_list
#         return jsonify(services)
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500


# @main.route('/api/update-service-status/<int:service_id>', methods=['POST'])
# def update_service_status(service_id):
#     try:
#         # Get the service by ID or return 404 if not found
#         service = Service.query.get_or_404(service_id)
        
#         # Toggle service status between ACTIVE and INACTIVE
#         service.status = "INAC" if service.status == "ACTV" else "ACTV"
        
#         # Commit the change to the database
#         db.session.commit()
        
#         # Invalidate the cache for all services if using Redis
#         redis_client.delete('all_service')
        
#         # Return a success response
#         return jsonify({'message': 'Service updated successfully!'}), 200
#     except Exception as e:
#         # Return error message in case of failure
#         return jsonify({'error': str(e)}), 500

    

# @main.route('/api/professionals')
# def get_professionals():
#     try:
#         professionals = redis_client.get('all_professionals')
#         if professionals:
#             professionals = json.loads(professionals)
#         else:
#             professionals = ServiceProfessional.query.all()
#             professionals_list = []
#             for professional in professionals:
#                 user_details = User.query.filter_by(user_id=professional.user_id).first()
#                 recruiter_data = {
#                     'service_professional_id': professional.service_professional_id,
#                     'approved_status': professional.approved_status,
#                     'file_path': professional.file_path,
#                     'user_details': {
#                         'firstname': user_details.firstname if user_details else None,
#                         'lastname': user_details.lastname if user_details else None,
#                         'email': user_details.email if user_details else None,
#                         'phone_number': user_details.phone_number if user_details else None,
#                         'status': user_details.status if user_details else None,
#                         'role': user_details.role if user_details else None
#                     }
#                 }
#                 professionals_list.append(recruiter_data)
#             redis_client.setex('all_professionals', 600, json.dumps(professionals_list))
#             professionals = professionals_list
        
#         return jsonify(professionals)
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500


# @main.route('/api/approve-professional/<int:professional_id>', methods=['POST'])
# def approve_professional(professional_id):
#     try:
#         professional = ServiceProfessional.query.get_or_404(professional_id)
#         professional.approved_status = 'APPROVED'
#         user = User.query.get_or_404(professional.user_id)
#         user.status = 'ACTV'
#         db.session.commit()
#         redis_client.delete('all_professionals')  # Cache invalidation
#         return jsonify({'message': 'Professional approved successfully!'}), 200
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'error': str(e)}), 500


# @main.route('/api/reject-professional/<int:professional_id>', methods=['POST'])
# def reject_professional(professional_id):
#     try:
#         professional = ServiceProfessional.query.get_or_404(professional_id)
#         professional.approved_status = 'REJECTED'
#         db.session.commit()
#         redis_client.delete('all_professionals')  # Cache invalidation
#         return jsonify({'message': 'Professional rejected successfully!'}), 200
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'error': str(e)}), 500


# # User APIs
# @main.route('/api/users')

# def get_users():
#     try:
#         users = User.query.all()
#         users_data = [user.to_dict() for user in users]
#         return jsonify(users_data)
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @main.route('/api/delete-user/<int:service_professional_id>', methods=['POST'])

# def delete_user(service_professional_id):
#     try:
#         service_professional = ServiceProfessional.query.get_or_404(service_professional_id)
#         user=User.query.get_or_404(service_professional.user_id)
#         user.status = "INAC" if user.status == "ACTV" else "ACTV"
#         db.session.commit()
#         redis_client.delete('all_professionals')
#         return jsonify({'message': 'User status updated successfully!'}), 200
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'error': str(e)}), 500

# # Service Requests APIs
# @main.route('/api/service-requests')

# def get_service_requests():
#     try:
#         service_requests = ServiceRequest.query.all()
#         service_requests_data = [request.to_dict() for request in service_requests]
#         return jsonify(service_requests_data)
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500


# @main.route('/api/service/<int:service_id>', methods=['GET'])
# def get_service(service_id):
#     service = Service.query.get_or_404(service_id)
#     return jsonify({
#         'service_id': service.service_id,
#         'name': service.name,
#         'base_price': service.base_price,
#         'required_time': service.required_time,
#         'description': service.description,
#         'status': service.status
#     })
# @main.route('/api/service/<int:service_id>', methods=['GET', 'POST'])
# def update_service(service_id):
#     # Clear Redis cache if necessary
#     if redis_client.delete('all_service'):
#         pass

#     # Fetch the service record
#     service = Service.query.get_or_404(service_id)

#     if request.method == 'GET':
#         # Return the service details as JSON
#         return jsonify({
#             "service_id": service.service_id,
#             "name": service.name,
#             "base_price": service.base_price,
#             "required_time": service.required_time,
#             "description": service.description
#         })

#     elif request.method == 'POST':
#         data = request.get_json()
#         if not data:
#             return jsonify({"message": "Invalid input"}), 400

#         # Validate the input
#         name = data.get('name')
#         base_price = data.get('base_price')
#         required_time = data.get('required_time')
#         description = data.get('description')

#         if not name or not isinstance(base_price, (int, float)) or not isinstance(required_time, int) or not description:
#             return jsonify({"message": "Invalid data format"}), 400

#         # Check if the service name is unique (excluding the current service)
#         existing_service = Service.query.filter(
#             Service.name == name, Service.service_id != service_id
#         ).first()

#         if existing_service:
#             return jsonify({"message": "A service with this name already exists."}), 400

#         try:
#             # Update the service details
#             service.name = name
#             service.base_price = base_price
#             service.required_time = required_time
#             service.description = description

#             # Commit the changes to the database
#             db.session.commit()
#             return jsonify({"message": "Service updated successfully!"}), 200

#         except Exception as e:
#             # Rollback in case of an error
#             db.session.rollback()
#             return jsonify({"message": f"An error occurred: {str(e)}"}), 500
        
# @main.route('/api/uploads/<filename>')
# def uploaded_file(filename):
#     return send_from_directory("", filename)


# @main.route('/api/admin-request')
# def admin_request():
#     serviceRequest=ServiceRequest.query.all()
#     serviceRequestData=[]
#     for service in serviceRequest:
#         requestData={
#             "service_id":service.service_id,
#             "service_name":service.professional.service_type,
#             "service_request_id":service.service_request_id,
#             "customer_name":service.customer.user.firstname,
#             "customer_city":service.customer.user.city,
#             "customer_pincode":service.customer.user.pincode,
#             "prof_name":service.professional.user.firstname,
#             "prof_city":service.professional.user.city,
#             "prof_pincode":service.professional.user.pincode,
#             "professional_name":service.professional.user.firstname,
#             "requested_date":service.date_of_request,
#             "contact_number":service.professional.user.phone_number,
#             "service_status":service.service_status,
#             "status":service.status
#         }
#         serviceRequestData.append(requestData)
#     return jsonify(serviceRequestData),200


# @main.route('/api/customer-request1/<int:id>')
# def customer_request1(id):
#     serviceRequest=ServiceRequest.query.filter_by(customer_id=id).all()
#     serviceRequestData=[]
#     for service in serviceRequest:
#         requestData={
#             "service_id":service.service_id,
#             "service_name":service.professional.service_type,
#             "service_request_id":service.service_request_id,
#             "customer_name":service.customer.user.firstname,
#             "customer_city":service.customer.user.city,
#             "customer_pincode":service.customer.user.pincode,
#             "prof_name":service.professional.user.firstname,
#             "prof_city":service.professional.user.city,
#             "prof_pincode":service.professional.user.pincode,
#             "professional_name":service.professional.user.firstname,
#             "requested_date":service.date_of_request,
#             "contact_number":service.professional.user.phone_number,
#             "service_status":service.service_status,
#             "status":service.status
#         }
#         serviceRequestData.append(requestData)
#     return jsonify(serviceRequestData),200


# @main.route('/api/prof-request1/<int:id>')
# def prof_request1(id):
#     serviceRequest=ServiceRequest.query.filter_by(service_professional_id=id).all()
#     serviceRequestData=[]
#     for service in serviceRequest:
#         requestData={
#             "service_id":service.service_id,
#             "service_name":service.professional.service_type,
#             "service_request_id":service.service_request_id,
#             "customer_name":service.customer.user.firstname,
#             "customer_city":service.customer.user.city,
#             "customer_pincode":service.customer.user.pincode,
#             "prof_name":service.professional.user.firstname,
#             "prof_city":service.professional.user.city,
#             "prof_pincode":service.professional.user.pincode,
#             "professional_name":service.professional.user.firstname,
#             "requested_date":service.date_of_request,
#             "contact_number":service.professional.user.phone_number,
#             "service_status":service.service_status,
#             "status":service.status
#         }
#         serviceRequestData.append(requestData)
#     return jsonify(serviceRequestData),200



# @main.route('/api/customer-request/<string:userId>')
# def customer_request(userId):
#     try:
#         # Filter service requests by userId
#         serviceRequests = ServiceRequest.query.filter_by(customer_id=userId).all()
#         serviceRequestData = []
        
#         for service in serviceRequests:
#             requestData = {
#                 "service_id": service.service_id,
#                 "service_name": service.professional.service_type,
#                 "service_request_id": service.service_request_id,
#                 "customer_name": service.customer.user.firstname,
#                 "professional_name": service.professional.user.firstname,
#                 "requested_date": service.date_of_request,
#                 "contact_number": service.professional.user.phone_number,
#                 "service_status": service.service_status,
#                 "status": service.status
#             }
#             serviceRequestData.append(requestData)
        
#         return jsonify(serviceRequestData), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# @main.route('/api/service_professionals/<int:service_id>')
# def service_professionals(service_id):
#     try:
#         # Querying ServiceProfessional along with User
#         professionals = db.session.query(ServiceProfessional, User) \
#             .join(User, ServiceProfessional.user_id == User.user_id) \
#             .filter(ServiceProfessional.service_id == service_id, ServiceProfessional.approved_status == 'APPROVED', User.status == "ACTV") \
#             .all()
        
#         result = []

#         # Loop through the query result which are tuples (ServiceProfessional, User)
#         for professional, user in professionals:
#             # Calculating the average rating
#             avg_rating = (
#                 db.session.query(db.func.avg(ServiceReviewAndRating.rating))
#                 .filter(
#                     ServiceReviewAndRating.service_professional_id == professional.service_professional_id,
#                     ServiceReviewAndRating.service_id == service_id
#                 )
#                 .scalar() or 0
#             )

#             result.append({
#                 'service_professional_id': professional.service_professional_id,
#                 'user': {
#                     'firstname': user.firstname,
#                     'lastname': user.lastname,
#                 },
#                 'base_price': professional.service.base_price,
#                 'service_type': professional.service_type,
#                 'experience': professional.experience,
#                 'average_rating': round(avg_rating, 2),
#             })

#         return jsonify({'professionals': result})
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500


# @main.route('/api/book_service', methods=['POST'])
# def book_service():
#     try:
#         data = request.get_json()
#         professional_id = data.get('professional_id')
#         service_id = data.get('service_id')
#         customerId = data.get('customerId')  # Optional remarks
#         userId = data.get('userId')  # Optional remarks

#         if not professional_id or not service_id:
#             return jsonify({'error': 'Professional ID and Service ID are required.'}), 400

#         # Prepare the batch request for Celery
#         service_request_batch = [
#             {
#                 'professional_id': professional_id,
#                 'service_id': service_id,
#                 'customer_id': customerId,
#                 'user_id': userId,
#                 'remarks': "remarks"
#             }
#         ]

#         # Send task to Celery
#         current_app.celery.send_task('app.tasks.process_service_booking', args=[service_request_batch])

#         flash('Service booking request has been sent for processing.', 'success')
#         return jsonify({'message': 'Service request is being processed!'}), 202

#     except Exception as e:
#         return jsonify({'error': str(e)}), 400


# @main.route('/api/close_request', methods=['POST'])
# def close_request():
#     try:
#         data = request.get_json()
#         service_request_id = data.get('service_request_id')
#         remarks = data.get('remarks')
#         rating = data.get('rating')
#         user_id = data.get('user_id')

#         service_request = ServiceRequest.query.get(service_request_id)
#         if service_request:
#             service_request.service_status = 'CLOSED'
#             service_request.date_of_completion = datetime.datetime.now()
#             db.session.commit()

#             review = ServiceReviewAndRating(
#                 customer_id=service_request.customer_id,
#                 service_professional_id=service_request.service_professional_id,
#                 service_request_id=service_request.service_request_id,
#                 service_id=service_request.service_id,
#                 remarks=remarks,
#                 rating=rating,
#                 created_by=user_id
#             )
#             db.session.add(review)
#             db.session.commit()

#             return jsonify({'message': 'Service request has been closed!'}), 200
#         else:
#             return jsonify({'error': 'Service request not found.'}), 404
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'error': str(e)}), 500


# @main.route('/api/professional-request/<string:userId>')
# def professional_request(userId):
#     try:
#         # Filter service requests by userId
#         closedServiceRequests = ServiceRequest.query.filter_by(service_professional_id=userId,service_status='CLOSED').all()

#         openServiceRequests = ServiceRequest.query.filter_by(service_professional_id=userId).all()
#         closedServiceRequestData = []
#         openServiceRequestData = []
        
#         for service in closedServiceRequests:
#             requestData = {
#                 "service_id": service.service_id,
#                 "service_name": service.professional.service_type,
#                 "service_request_id": service.service_request_id,
#                 "customer_name": service.customer.user.firstname,
#                 "requested_date": service.date_of_request,
#                 "contact_number": service.customer.user.phone_number,
#                 "service_status": service.service_status,
#                 "city": service.customer.user.city,
#                 "pin_code": service.customer.user.pincode,
#                 "status": service.status
#             }
#             closedServiceRequestData.append(requestData)

#         for service in openServiceRequests:
#             if service.service_status != 'CLOSED':
#                 requestData = {
#                     "service_id": service.service_id,
#                     "service_name": service.professional.service_type,
#                     "service_request_id": service.service_request_id,
#                     "customer_name": service.professional.user.firstname,
#                     "requested_date": service.date_of_request,
#                     "contact_number": service.professional.user.phone_number,
#                     "service_status": service.service_status,
#                     "city": service.professional.user.city,
#                     "pin_code": service.professional.user.pincode,
#                     "status": service.status
#                 }
#                 openServiceRequestData.append(requestData)
#         data={
#             "closedServiceRequestData":closedServiceRequestData,
#             "openServiceRequestData":openServiceRequestData
#         }
#         return jsonify(data), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
    


# @main.route('/api/reject-request/<int:service_request_id>', methods=['POST'])
# def reject_request(service_request_id):
#     try:
#         # Get the service request by ID
#         service_request = ServiceRequest.query.get_or_404(service_request_id)

#         # Update the approved_status to 'RJCT'
#         service_request.service_status = 'RJCT'

#         # Commit the change to the database
#         db.session.commit()

#         # Return success response
#         return jsonify({'message': 'Request rejected successfully!'}), 200
#     except Exception as e:
#         db.session.rollback()  # Rollback the transaction on error
#         print(f"Error rejecting request: {str(e)}")  # Debugging log
#         return jsonify({'error': str(e)}), 500


# @main.route('/api/approve-request/<int:service_request_id>', methods=['POST'])
# def approve_request(service_request_id):
#     try:
#         # Get the service request by ID
#         service_request = ServiceRequest.query.get_or_404(service_request_id)

#         # Update the approved_status to 'OPEN'
#         service_request.service_status = 'OPEN'

#         # Commit the change to the database
#         db.session.commit()

#         # Return success response
#         return jsonify({'message': 'Request approved successfully!'}), 200
#     except Exception as e:
#         db.session.rollback()  # Rollback the transaction on error
#         print(f"Error approving request: {str(e)}")  # Debugging log
#         return jsonify({'error': str(e)}), 500

# @main.route('/api/professional-chart/<int:service_professional_id>', methods=['GET'])
# def get_professional_chart(service_professional_id):
#     try:
#         # Fetch average rating of service professionals
#         rating_data = db.session.query(
#             ServiceProfessional.service_professional_id,
#             db.func.avg(ServiceReviewAndRating.rating).label('average_rating')
#         ).join(ServiceReviewAndRating, ServiceProfessional.service_professional_id == ServiceReviewAndRating.service_professional_id)\
#         .filter(
#             ServiceReviewAndRating.status == 'ACTV',
#             ServiceProfessional.service_professional_id == service_professional_id
#         )\
#         .group_by(ServiceProfessional.service_professional_id).all()

#         ratings = [{"service_professional_id": res[0], "average_rating": res[1]} for res in rating_data]

#         # Fetch service request status summary
#         status_summary = db.session.query(
#             ServiceRequest.service_status,
#             db.func.count(ServiceRequest.service_request_id).label('total')
#         ).filter(ServiceRequest.service_professional_id == service_professional_id)\
#         .group_by(ServiceRequest.service_status).all()

#         statuses = [{"status": res[0], "total": res[1]} for res in status_summary]

#         # Combine both results
#         data = {
#             "ratings": ratings,
#             "statuses": statuses
#         }

#         return jsonify(data)
    
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


# @main.route('/api/customer-chart<int:customer_id>', methods=['GET'])
# def get_customer_chart(customer_id):
#     try:
#         # Fetch service request status summary
#         status_summary = db.session.query(
#             ServiceRequest.service_status,
#             db.func.count(ServiceRequest.service_request_id).label('total')
#         ).filter(ServiceRequest.customer_id == customer_id).group_by(ServiceRequest.service_status).all()

#         statuses = [{"status": res[0], "total": res[1]} for res in status_summary]

#         # Combine both results
#         data = {
#             "statuses": statuses
#         }

#         return jsonify(data)

#     except Exception as e:
#         return jsonify({'error': str(e)}), 400


# @main.route('/api/admin-chart', methods=['GET'])
# def get_admin_chart():
#     try:
#         # Fetch average rating of service professionals
#         rating_data = db.session.query(
#             ServiceProfessional.service_professional_id,
#             db.func.avg(ServiceReviewAndRating.rating).label('average_rating')
#         ).join(ServiceReviewAndRating, ServiceProfessional.service_professional_id == ServiceReviewAndRating.service_professional_id)\
#         .filter(ServiceReviewAndRating.status == 'ACTV')\
#         .group_by(ServiceProfessional.service_professional_id).all()

#         ratings = [{"service_professional_id": res[0], "average_rating": res[1]} for res in rating_data]

#         # Fetch service request status summary
#         status_summary = db.session.query(
#             ServiceRequest.service_status,
#             db.func.count(ServiceRequest.service_request_id).label('total')
#         ).group_by(ServiceRequest.service_status).all()

#         statuses = [{"status": res[0], "total": res[1]} for res in status_summary]

#         # Combine both results
#         data = {
#             "ratings": ratings,
#             "statuses": statuses
#         }
#     except Exception as e:
#         flash(f"An error occurred: {str(e)}", 'danger')
#         data = {"ratings": [], "statuses": []}

#     return jsonify(data)
