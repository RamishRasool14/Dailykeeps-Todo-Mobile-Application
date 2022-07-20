package com.tajir.dailykeeps.data.StateModels

import com.tajir.dailykeeps.data.api.interfeces.models.RegisterResponse
import retrofit2.Response


data class RegisterState(
    val first_name : String = "",
    val last_name : String = "",
    val email : String = "",
    val password : String = "",
    val loading : Boolean = false,
    val err : String = "",
    var register_response : Response<RegisterResponse>? = null
) {
}
