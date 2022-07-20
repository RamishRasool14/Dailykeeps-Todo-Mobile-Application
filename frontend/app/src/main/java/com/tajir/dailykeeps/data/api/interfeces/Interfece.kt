package com.tajir.dailykeeps.data.api.interfeces

import com.tajir.dailykeeps.data.api.interfeces.models.*
import retrofit2.http.POST
import retrofit2.Response
import retrofit2.http.Body

interface Interface {
    @POST("/register_user")
    suspend fun register(
        @Body data : Register
    ): Response<RegisterResponse>

    @POST("/login_user")
    suspend fun login(
        @Body data : Login
    ): Response<LoginResponse>

    @POST("/get_task")
    suspend fun get_task(
        @Body data : GetTask
    ): Response<TaskResponse>

    @POST("/delete_task")
    suspend fun delete_task(
        @Body data : DeleteTask
    ): Response<DeleteResponse>

    @POST("/edit_task")
    suspend fun edit_task(
        @Body data : EditTask
    ): Response<EditResponse>


    @POST("/create_task")
    suspend fun add_task(
        @Body data : AddTask
    ): Response<AddResponse>




}
