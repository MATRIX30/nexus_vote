"""
Views module for the Nexus Vote polling application.

This module contains all the view classes and functions that handle HTTP requests
for the Nexus Vote system. It provides RESTful API endpoints for managing users,
polls, votes, and registrations in the decentralized voting platform.

The views are built using Django REST Framework (DRF) and follow RESTful principles
for API design. Each view handles specific resources and provides appropriate
HTTP methods for CRUD operations.

Classes:
    UserView: Handles individual user operations (GET, PUT)
    UserListViews: Handles user collection operations (GET list)

Functions:
    home: Provides a simple status endpoint for the application

Author: MATRIX30
Project: Nexus Vote - Decentralized Voting Platform
Version: 1.0
"""

from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from polling_app.models import User, Poll, Registration, Vote, VoteOption
from polling_app.serializer import userSerializer, pollSerializer


# Create your views here.
def home(request):
    """
    Home view for the Nexus Vote polling application.
    
    Provides a simple status endpoint to verify that the application is running.
    
    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.
        
    Returns:
        HttpResponse: A simple HTTP response indicating the application status.
        
    Example:
        GET /api/
        Response: {"Status Ok Started!"}
    """
    data = {"Status Ok Started!"}
    return HttpResponse(data)


class UserView(APIView):
    """
    API view for managing individual user operations.
    
    Provides endpoints for retrieving, updating, and managing specific users
    in the Nexus Vote system. This view handles operations on individual users
    identified by their unique ID.
    
    Attributes:
        None
        
    Methods:
        get: Retrieve user details by ID
        put: Update user information (placeholder)
        
    Example URLs:
        GET /api/user/1/ - Get user with ID 1
        PUT /api/user/1/ - Update user with ID 1
    """
    
    def get(self, request, id):
        """
        Retrieve user details by user ID.
        
        Fetches a specific user from the database and returns their details
        in serialized format. The user is identified by their unique ID.
        
        Args:
            request (Request): DRF request object containing request metadata.
            id (int): The unique identifier of the user to retrieve.
            
        Returns:
            Response: DRF Response object containing:
                - On success: Serialized user data (200 OK)
                - On error: Error message with appropriate HTTP status code
                
        Raises:
            User.DoesNotExist: When no user exists with the provided ID.
            
        Example:
            GET /api/user/1/
            Response: {
                "id": 1,
                "username": "john_doe",
                "email": "john@example.com",
                "role": "CLIENT"
            }
        """
        user = User.objects.get(id=id)
        serialized_user = userSerializer(user)
        
        return Response(serialized_user.data)
    
    def put(self, request, id):
        """
        Update user information by user ID.
        
        Updates an existing user's information with the provided data. This method
        handles partial or complete updates of user records. All fields are optional
        for updates except those with validation constraints.
        
        Args:
            request (Request): DRF request object containing update data in request.data.
                            Acceptable fields: username, email, password_hash, role
            id (int): The unique identifier of the user to update.
            
        Returns:
            Response: DRF Response object containing:
                - On success (200): Updated user data
                - On not found (404): Error message when user doesn't exist
                - On validation error (400): Validation error details
                - On server error (500): Error message for unexpected issues
                
        Example:
            PUT /api/user/1/
            Request Body: {
                "username": "updated_username",
                "email": "newemail@example.com",
                "role": "ADMIN"
            }
            
            Success Response (200): {
                "id": 1,
                "username": "updated_username",
                "email": "newemail@example.com",
                "role": "ADMIN"
            }
            
            Error Response (404): {
                "error": "User not found"
            }
            
            Validation Error (400): {
                "email": ["Enter a valid email address."],
                "username": ["This field must be unique."]
            }
        """
        try:
            instance = User.objects.get(id=id)
            serialized_user = userSerializer(instance=instance, data=request.data, partial=True)
            
            if serialized_user.is_valid():
                serialized_user.save()
                return Response(
                    serialized_user.data,
                    status=status.HTTP_200_OK
                    )
            else:
                # Return validation errors
                return Response(
                    serialized_user.errors, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
                    return Response(
            {
                'error': 'An error occurred while updating the user.',
                'details': str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
            
    def delete(self, request, id):
        """
        Delete specific user by ID.
        
        Removes a user from the system. Note: This will cascade delete
        related records (polls, votes, registrations) based on model
        foreign key constraints.
        
        Args:
            request (Request): DRF request object
            id (int): User ID to delete
            
        Returns:
            Response: 204 No Content on success, 404 if user not found
        """
        try:
            user = User.objects.get(id=id)
            user.delete()
            return Response(
                {'Status': 'User deleted successfully'}, 
                status=status.HTTP_204_NO_CONTENT
            )
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )


class UserListViews(APIView):
    """
    API view for managing user collections and list operations.
    
    Provides endpoints for retrieving lists of users and performing
    bulk operations on user collections. This view handles operations
    that affect multiple users or provide user listings.
    
    Attributes:
        None
        
    Methods:
        get: Retrieve list of all users
        
    Example URLs:
        GET /api/users/ - Get list of all users
    """
    
    def get(self, request):
        """
        Retrieve a list of all users in the system.
        
        Fetches all users from the database and returns them in serialized format.
        This endpoint provides a complete listing of all registered users in the
        Nexus Vote system.
        
        Args:
            request (Request): DRF request object containing request metadata.
            
        Returns:
            Response: DRF Response object containing:
                - Serialized list of all users
                - HTTP 200 OK status on success
                
        Note:
            The current implementation has a logical issue with serializer
            validation that should be addressed. The serializer should use
            many=True for multiple objects and validation check is redundant
            for read operations.
            
        Example:
            GET /api/users/
            Response: [
                {
                    "id": 1,
                    "username": "john_doe",
                    "email": "john@example.com",
                    "role": "CLIENT"
                },
                {
                    "id": 2,
                    "username": "admin_user",
                    "email": "admin@example.com",
                    "role": "ADMIN"
                }
            ]
            
        Todo:
            - Fix serializer usage with many=True parameter
            - Remove unnecessary validation check for read operations
            - Add pagination for large user lists
            - Add filtering and search capabilities
        """
        users = User.objects.all()
        
        serialized_users = userSerializer(users, many=True)
        return Response(serialized_users.data)
    
    def post(self, request):
        serialized_user = userSerializer(data=request.data)
        if serialized_user.is_valid():
            serialized_user.save()
            return Response(serialized_user.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serialized_user.errors, status=status.HTTP_400_BAD_REQUEST)


# class based views

@api_view(["GET","PUT"])
def PollView(request, id):
    """
    Retrieve poll details by poll ID.
    
    Args:
        request: DRF request object
        id: Poll ID to retrieve
        
    Returns:
        Response: Poll data or error message
    """
    if request.method == "GET":
        try:
            poll = Poll.objects.get(id=id)
            serialized_poll = pollSerializer(poll)
            return Response(serialized_poll.data)
        except Poll.DoesNotExist:
            return Response({"Error":f"Object with id {id} doesn't exist"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"Error":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if request.method == "PUT":
        # try to get object with id if it fails report failure
        try:
            poll = Poll.objects.get(pk=id)
            serialized_poll = pollSerializer(poll)
            
        except Poll.DoesNotExist:
            return Response({"Error":f"Object with id {id} doesn't exist"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"Error":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET", "POST"])
def PollViewList(request):
    
    if request.method == "GET":
        try:
            poll_list = Poll.objects.all()
            serialized_poll = pollSerializer(poll_list, many=True)
            return Response(serialized_poll.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": "An error occurred while creating the poll"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    if request.method == "POST":
        try:
            # capture the data and build a new poll object
            
            serialized_poll = pollSerializer(data=request.data)
            if serialized_poll.is_valid():
                serialized_poll.save()
                return Response(serialized_poll.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serialized_poll.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"Error":f"Unable to create new Poll {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
