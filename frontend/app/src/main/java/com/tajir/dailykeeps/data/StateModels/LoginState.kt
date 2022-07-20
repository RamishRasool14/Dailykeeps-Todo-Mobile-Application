package com.tajir.dailykeeps.data.StateModels

import com.tajir.dailykeeps.data.api.interfeces.models.LoginResponse
import retrofit2.Response

data class LoginState(
    val first_name : String = "",
    val last_name : String = "",
    val email : String = "",
    val password : String = "",
    val loading : Boolean = false,
    var token : String = "",
    val err : String = "",
    var status : String = "",
    val login_response : Response<LoginResponse> ? = null
) {
    fun updateToken()
    {
        if (login_response?.body() != null && login_response!!.body()?.description == "successfully logged in")
        {
            token = login_response!!.body()!!.token
        }
    }
}

