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
                $window.location.href = 'http://localhost:5000/student_management_system/teacher';
            }
            else if(response.type == "admin"){
                console.log("Admin loggin")
                $window.location.href = 'http://localhost:5000/student_management_system/admin';
            }
            else if(response.type == "student"){
                console.log("Student loggin")
                $window.location.href = 'http://localhost:5000/student_management_system/student';
            }
            else{
                swal(response)
            }

        })
        .error(function(response){
            console.log("Error")

        });
    }

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
            console.log(response)
            swal(response)
        })
        .error(function(response){
            console.log(response)
            swal(response)
        });

    }

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
            swal(response)
            console.log(response)
            console.log($scope.newUser)

        })
        .error(function(response){
            console.log(response)
            swal(response)
        });

    }
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
            swal(response)
        })
        .error(function(response){
            console.log(response)
            swal(response)
        });

    }


    }]);

})();