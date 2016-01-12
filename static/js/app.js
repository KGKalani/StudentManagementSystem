/*<header>
<title>app.js</title>
<description>Use to handle client side data and send request to sever side</description>
<copyRight>Copyright (c) 2015</copyRight>
<createdOn>2015-12-31</createdOn>
<author>Gayathri Kalani</author>
</header>*/

(function(){

    'use strict';

    var app = angular.module("app", [])
    app.controller('appController',['$scope', '$http','$window', function($scope, $http, $window){
    $scope.newUser;

    //Send loggin request
    $scope.getLoggin = function(){
        var _url = "http://localhost:5000/student_management_system/userloggin";

        $http({
            url: _url,
            method: 'POST',
            header:{
                'Content-Type': 'application/json'
            },
            data:{
                username: $scope.username,
                userPassword: $scope.password
            }
        })
        .success(function(response){
            if(response.type == "teacher"){
                console.log("Teacher loggin")
                $scope.newUser = response.name
                $window.location.href = 'http://localhost:5000/student_management_system/teacher';
            }
            else if(response.type == "admin"){
                console.log("Admin loggin")
                $scope.newUser = response.name
                $window.location.href = 'http://localhost:5000/student_management_system/admin';
            }
            else if(response.type == "student"){
                console.log("Student loggin")
                $window.location.href = 'http://localhost:5000/student_management_system/student';
            }
            else{
                swal(response.status)
            }

        })
        .error(function(response){
            console.log("Error")
            console.log(response)
            swal(response.status)
        });
    }

    //Send sigmup request
    $scope.singUpUser = function(){
        var _url = "http://localhost:5000/student_management_system/userSignUp";

        $http({
            url: _url,
            method: 'POST',
            header: {
                 'Content-Type': 'application/json'
            },
            data:{
                userNIC: $scope.userNIC,
                username: $scope.username,
                userPassword: $scope.password,
                userType: $scope.userType
            }
        })
        .success(function(response){
            console.log(response.status)
            swal(response.status)
        })
        .error(function(response){
            console.log(response.status)
            swal(response.status)
        });

    }

    //Send request for user registration( Teacher and student)
    $scope.otherUsersRegistration = function(){
        var _url = "http://localhost:5000/student_management_system/otherUsersRegistration";
        $http({
            url: _url,
            method: 'POST',
            header: {
                 'Content-Type': 'application/json'
            },
            data:{
                user_id: $scope.userId,
                name: $scope.name,
                userNIC: $scope.userNIC,
                userType: $scope.userType
            }
        })
        .success(function(response){
            swal(response.status)
            console.log(response)
            console.log($scope.newUser)

        })
        .error(function(response){
            console.log(response)
            swal(response.status)
        });

    }

    //Send request for user registration
   $scope.studentRegistration = function(){
        var _url = "http://localhost:5000/student_management_system/studentRegistration";
        $http({
            url: _url,
            method: 'POST',
            header: {
                 'Content-Type': 'application/json'
            },
            data:{
                user_id: $scope.userId,
                name: $scope.name,
                grade: $scope.grade
            }
        })
        .success(function(response){
            console.log(response)
            swal(response.status)
        })
        .error(function(response){
            console.log(response)
            swal(response.status)
        });
    }

    //Send request to register classes
    $scope.classRegistration = function(){
        var _url = "http://localhost:5000/student_management_system/classRegistration";
        $http({
            url: _url,
            method: 'POST',
            header: {
                 'Content-Type': 'application/json'
            },
            data:{
                t_id: $scope.teacherId,
                class_id: $scope.classId,
                grade: $scope.grade,
                subject: $scope.subject
            }
        })
        .success(function(response){
            console.log(response.status)
            swal(response.status)
        })
        .error(function(response){
            console.log(response)
            swal(response.status)
        });
    }
    $scope.scheduleRegistration = function(){
    var _url = "http://localhost:5000/student_management_system/scheduleRegistration";
        $http({
            url: _url,
            method: 'POST',
            header: {
                 'Content-Type': 'application/json'
            },
            data:{
                class_id: $scope.classId,
                schedule_id: $scope.sheduleId,
                day: $scope.day,
                start_time: $scope.start_time,
                end_time:$scope.end_time
            }
        })
        .success(function(response){
            console.log(response.status)
            swal(response.status)
        })
        .error(function(response){
            console.log(response)
            swal(response.status)
        });
    }

    }]);


})();