package com.tajir.dailykeeps.data.api.interfeces.models

import java.util.*

data class RegisterResponse(
    val error : String = "",
    val description : String = ""
)

data class TaskResponse(
    val data : List<Task> = emptyList(),
    val description : String = ""
)

data class LoginResponse(
    val token : String = "",
    val description : String = ""
)

data class DeleteResponse(
    val description : String = ""
)

data class EditResponse(
    val description : String = ""
)

data class AddResponse(
    val description : String = ""
)
