package com.tajir.dailykeeps.viewmodels

import android.app.Application
import android.content.Context
import android.os.Build
import androidx.annotation.RequiresApi
import androidx.compose.runtime.compositionLocalOf
import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewModelScope
import com.tajir.dailykeeps.data.StateModels.TaskState
import com.tajir.dailykeeps.data.api.RetrofitInstance
import com.tajir.dailykeeps.data.api.interfeces.models.*
import com.tajir.dailykeeps.ui.session.Session
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.launch
import retrofit2.Response
import java.time.LocalDateTime
import java.time.format.DateTimeFormatter


class TaskViewModel(mApplication: Application, mContext: Context) : ViewModel() {
    var cntxt: Context = mContext
    var session: Session = Session(mContext)
    val taskState = MutableStateFlow(TaskState())

    private fun setErr(msg: String)
    {
        taskState.value = taskState.value.copy(
            msg = msg
        )
    }

    fun updateResponse(data: Response<TaskResponse>)
    {
        updateTask(data.body()?.data)
        taskState.value = taskState.value.copy(
            task_response = data
        )
    }

    fun updateText(text: String) {
        taskState.value = taskState.value.copy(
            runningText = text
        )
    }

    fun updateToken(token: String)
    {
        taskState.value = taskState.value.copy(
            token = token
        )
        session.setusename(token)
    }

    fun updateTask(data: List<Task>?)
    {
        var sorted_data = data?.sortedBy{ it.due_time }
        taskState.value = taskState.value.copy(
            tasks = sorted_data!!
        )
    }

    fun deleteTask(id: String)
    {
        viewModelScope.launch {
            val data = DeleteTask(
                id = id
            )
            try {
                val res = RetrofitInstance().Api.delete_task(data)
                getTask()
            } catch(e : Exception) {
                setErr("Check your internet connection.")
            }
        }

    }

    @RequiresApi(Build.VERSION_CODES.O)
    fun updateSelectedTask(task: Task)
    {
        val formatter = DateTimeFormatter.ofPattern("EEE, dd MMM yyyy HH:mm:ss zzz")
        val new_formatter = DateTimeFormatter.ofPattern("EEE, dd MMM yyyy HH:mm:ss")

        taskState.value = taskState.value.copy(
            selectedTask = task!!
        )
        taskState.value = taskState.value.copy(
            localDateTime = LocalDateTime.parse(taskState.value.selectedTask?.due_time, formatter).format(new_formatter)
        )
    }

    @RequiresApi(Build.VERSION_CODES.O)
    fun editTaskStatus(task: Task)
    {
        val formatter = DateTimeFormatter.ofPattern("EEE, dd MMM yyyy HH:mm:ss zzz")
        val newformatter = DateTimeFormatter.ofPattern("EEE, dd MMM yyyy HH:mm:ss")
        viewModelScope.launch {

            val data = EditTask(
                token = taskState.value.token!!,
                id = task.id,
                description = task.description,
                due_time = LocalDateTime.parse(taskState.value.selectedTask?.due_time, formatter).format(newformatter).toString(),
                done = if (task.done) "false" else "true",
            )
            try {
                val res = RetrofitInstance().Api.edit_task(data)
                getTask()
            } catch(e : Exception) {
                setErr("Check your internet connection.")
            }
        }
    }

    fun editTaskDescription(task: Task)
    {
        viewModelScope.launch {
            val data = EditTask(
                token = taskState.value.token!!,
                id = task.id,
                description = taskState.value.runningText,
                due_time = taskState.value.localDateTime!!,
                done = task.done.toString(),
            )
            try {
                val res = RetrofitInstance().Api.edit_task(data)
                getTask()
            } catch(e : Exception) {
                setErr("Check your internet connection.")
            }
            updateText("")
        }
    }

    fun createTask()
    {
        if (taskState.value.runningText != "")
        {
            viewModelScope.launch {
                val data = AddTask(
                    token = taskState.value.token!!,
                    description = taskState.value.runningText,
                )
                try {
                    val res = RetrofitInstance().Api.add_task(data)
                    getTask()
                } catch(e : Exception) {
                    setErr("Check your internet connection.")
                }
            }

        }
    }

    @RequiresApi(Build.VERSION_CODES.O)
    fun updateDueDate(localDateTime: LocalDateTime)
    {
        val new_formatter = DateTimeFormatter.ofPattern("EEE, dd MMM yyyy HH:mm:ss")
        taskState.value = taskState.value.copy(
            localDateTime = localDateTime.format(new_formatter)
        )

    }

    fun updateNew(value : Int)
    {
        taskState.value = taskState.value.copy(
            newTask = value
        )
    }

    fun getTask(day: String = "")
    {
        viewModelScope.launch {
            val data = GetTask(
                token = taskState.value.token!!,
                day = day,
            )
            try {
                val res = RetrofitInstance().Api.get_task(data)
                updateResponse(res)
            } catch(e : Exception) {
                setErr("Check your internet connection.")
            }
        }
    }
}

class MyViewModelFactory(application: Application, context: Context) :
    ViewModelProvider.Factory {
    private val mApplication: Application
    private val mContext: Context
    override fun <T : ViewModel?> create(modelClass: Class<T>): T {
        return TaskViewModel(mApplication, mContext) as T
    }

    init {
        mApplication = application
        mContext = context
    }
}

val TaskState by lazy {
    compositionLocalOf<TaskViewModel> {
        error("Task Contexts not found.")
    }
}
