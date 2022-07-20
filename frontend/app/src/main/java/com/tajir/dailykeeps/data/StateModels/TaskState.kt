package com.tajir.dailykeeps.data.StateModels

import com.tajir.dailykeeps.data.api.interfeces.models.RegisterResponse
import com.tajir.dailykeeps.data.api.interfeces.models.Task
import com.tajir.dailykeeps.data.api.interfeces.models.TaskResponse
import retrofit2.Response
import java.time.LocalDateTime

data class TaskState constructor(
    val tasks: List<Task?> = emptyList(),
    val loading: Boolean = false,
    val selectedTask: Task? = null,
    val msg: String? = null,
    var task_response : Response<TaskResponse>? = null,
    var token: String? = null,
    var runningText: String = "",
    var newTask: Int = 0,
    var localDateTime: String? = null,
)
{

}