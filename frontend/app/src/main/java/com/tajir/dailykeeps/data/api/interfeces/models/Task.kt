package com.tajir.dailykeeps.data.api.interfeces.models

import java.time.LocalDateTime

data class Task(
    val creation_time: String,
    val description: String,
    val due_time: String,
    val id: String,
    val done: Boolean,
    val owner_id: String,
)

data class GetTask(
    val token: String,
    val day: String? = "",
)

data class DeleteTask(
    val id: String
)

data class EditTask(
    val due_time: String,
    val done: String,
    val description: String,
    val token: String,
    val id: String,
)

data class AddTask(
    val description: String,
    val token: String,
)


