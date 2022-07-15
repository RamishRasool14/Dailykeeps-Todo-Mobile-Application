package com.tajir.dailykeeps.ui

import android.app.DatePickerDialog
import android.app.TimePickerDialog
import android.content.Context
import android.os.Build
import androidx.annotation.RequiresApi
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.material.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.navigation.NavController
import com.tajir.dailykeeps.data.api.interfeces.models.Task
import com.tajir.dailykeeps.ui.components.InputField
import com.tajir.dailykeeps.viewmodels.TaskState
import java.time.LocalDateTime
import java.time.LocalTime
import java.util.*

@RequiresApi(Build.VERSION_CODES.O)
@Composable
fun TaskScreen(
    navController: NavController
) {
    val materialBlue700= Color(0xFF1976D2)
    val scaffoldState = rememberScaffoldState(rememberDrawerState(DrawerValue.Closed))
    val scope = rememberCoroutineScope()
    val taskStateClass = TaskState.current
    val taskState = TaskState.current.taskState.collectAsState().value

    val context = LocalContext.current
    val dueDate = LocalDateTime.now().with(LocalTime.MAX)

    Scaffold(
        scaffoldState = scaffoldState,
        topBar = { TopAppBar(navigationIcon = {
            IconButton(onClick = { }) {
                Icon(
                    Icons.Filled.AccountCircle, contentDescription = "Anything", modifier = Modifier
                        .clickable(onClick = {
                            navController.navigate("main")
                        })
                        .size(30.dp)
                )
            }
        }, backgroundColor = materialBlue700, title = { Text("Tasks", fontWeight = FontWeight.Bold ,fontSize = 35.sp, modifier = Modifier.width(220.dp))

            IconButton(onClick = { }) {
                Icon(Icons.Filled.Close, contentDescription = "Previous", modifier = Modifier
                    .clickable(onClick = {
                        navController.navigate("main")
                    })
                    .size(30.dp).width(200.dp))
            }

            IconButton(onClick = { }) {
                Icon(Icons.Filled.Check, contentDescription = "Okay", modifier = Modifier
                    .clickable(onClick = {
                        if (taskState.newTask == 1) {
                            taskStateClass.createTask()
                            taskStateClass.updateNew(0)
                        } else {
                            taskStateClass.editTaskDescription(taskState.selectedTask!!)
                        }
                        navController.navigate("main")
                    })
                    .size(30.dp))
            }

        }
        )  },
        content = {  Content() },
        floatingActionButtonPosition = FabPosition.End,
        floatingActionButton = { FloatingActionButton(onClick = {
            taskStateClass.updateText("")
            taskStateClass.updateNew(1)
            navController.navigate("task_edit")
        }){
            IconButton(onClick = { }) {
                Icon(Icons.Filled.CalendarToday, contentDescription = "Calender", modifier = Modifier
                    .clickable(onClick = {
                        selectDateTime(
                            context,
                            dueDate,
                            { taskStateClass.updateDueDate(localDateTime = it) })
                    })
                    .size(30.dp))
            }
        } }
    )
}

@Composable
fun Content()
{
    val taskStateClass = TaskState.current
    val taskState = TaskState.current.taskState.collectAsState().value
    Column( ) {
        Row() {
            Text(text = "Due:", fontWeight = FontWeight.Bold, fontSize = 20.sp, modifier = Modifier.width(70.dp))
            Text(text = taskState.localDateTime.toString() , fontSize = 15.sp, modifier = Modifier.width(150.dp))
            Text(text = "Status:", fontWeight = FontWeight.Bold, fontSize = 20.sp, modifier = Modifier.width(80.dp))
            Text(text = if(taskState.selectedTask!!.done) "Completed" else "Incomplete", fontSize = 15.sp, color = if(taskState.selectedTask!!.done) Color.Green else Color.Red , modifier = Modifier.padding(top = 5.dp))
        }
        TextField(value = taskState.runningText, onValueChange = { taskStateClass.updateText(text = it) }, Modifier.fillMaxSize() )
    }

}

@RequiresApi(Build.VERSION_CODES.O)
fun selectDateTime(
    context: Context,
    dt: LocalDateTime,
    changedCallBack: (due_date: LocalDateTime) -> Unit
) {

    val startYear = dt.year
    val startMonth = dt.monthValue
    val startDay = dt.dayOfMonth
    val startHour = dt.hour
    val startMinute = dt.minute

    DatePickerDialog(context, { _, year, month, day ->
        TimePickerDialog(context, { _, hour, minute ->
            val pickedDateTime = Calendar.getInstance()
            pickedDateTime.set(year, month, day, hour, minute)

            val dt = LocalDateTime.ofInstant(
                pickedDateTime.toInstant(),
                pickedDateTime.timeZone.toZoneId()
            )
            changedCallBack(dt)
        }, startHour, startMinute, false).show()
    }, startYear, startMonth, startDay).show()
}
