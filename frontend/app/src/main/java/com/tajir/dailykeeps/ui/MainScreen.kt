package com.tajir.dailykeeps.ui

import android.os.Build
import androidx.annotation.RequiresApi
import androidx.compose.animation.animateContentSize
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.material.*
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.AccountCircle
import androidx.compose.material.icons.filled.Logout
import androidx.compose.material.icons.filled.Menu
import androidx.compose.material.icons.filled.Refresh
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Rect
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Outline
import androidx.compose.ui.graphics.Shape
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.Density
import androidx.compose.ui.unit.LayoutDirection
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.navigation.NavController
import com.tajir.dailykeeps.data.api.interfeces.models.Task
import com.tajir.dailykeeps.ui.components.TaskCard
import com.tajir.dailykeeps.viewmodels.TaskState
import kotlinx.coroutines.launch

//@SuppressLint("CoroutineCreationDuringComposition")
//@RequiresApi(Build.VERSION_CODES.O)
@RequiresApi(Build.VERSION_CODES.O)
@Composable
fun MainScreen(
    navController: NavController
) {
    Column(
        modifier = Modifier
    ) {

        val materialBlue700= Color(0xFF1976D2)
        val scaffoldState = rememberScaffoldState(rememberDrawerState(DrawerValue.Closed))
        val scope = rememberCoroutineScope()

        val taskStateClass = TaskState.current
        val taskState = TaskState.current.taskState.collectAsState().value

        Scaffold(
            scaffoldState = scaffoldState,
            topBar = { TopAppBar(navigationIcon = {
                IconButton(onClick = { }) {
                    Icon(Icons.Filled.AccountCircle, contentDescription = "Anything", modifier = Modifier.clickable(onClick = {
//                        navController.navigate("profile_page")
                    }).size(30.dp).weight(1f)
                    )
                }
            }, backgroundColor = materialBlue700, title = { Text("Tasks", fontWeight = FontWeight.Bold ,fontSize = 35.sp, modifier = Modifier.width(220.dp))

                IconButton(onClick = { }) {
                    Icon(Icons.Filled.Refresh, contentDescription = "Refresh", modifier = Modifier.clickable(onClick = {
                        taskStateClass.getTask()
                    }).width(50.dp).size(30.dp).weight(1f))
                }
                IconButton(onClick = { }) {
                    Icon(Icons.Filled.Logout, contentDescription = "Logout", modifier = Modifier.clickable(onClick = {
                        navController.navigate("login")
                    }).size(30.dp).weight(1f))
                }

            }
            )  },
            floatingActionButtonPosition = FabPosition.End,
            floatingActionButton = { FloatingActionButton(onClick = {
                taskStateClass.updateText("")
                taskStateClass.updateNew(1)
                navController.navigate("task_edit")
            }){
                Text("+" ,fontSize = 35.sp)
            } },
            content = { TaskContent(taskState.tasks, navController ) },
        )
        
    }
}

@Composable
fun customShape(): Shape {
    val value = object : Shape {
        override fun createOutline(
            size: Size,
            layoutDirection: LayoutDirection,
            density: Density
        ): Outline {
            return Outline.Rectangle(
                Rect(
                    left = 0f,
                    top = 0f,
                    right = size.width * 1 / 3,
                    bottom = size.height
                )
            )
        }
}
    return value
}

@RequiresApi(Build.VERSION_CODES.O)
@Composable
fun TaskContent(
    tasks: List<Task?>,
    navController: NavController,
) {
    val taskStateClass = TaskState.current
    Column(modifier = Modifier) {
        if (tasks.isEmpty()) {
            Row(horizontalArrangement = Arrangement.Center) {
                Text(
                    text = "No Task Found.",
                    modifier = Modifier.padding(horizontal = 16.dp, vertical = 2.dp)
                )
            }
        } else {
            LazyColumn {
                items(tasks) { task ->
                    if (task != null) {
                        TaskCard(
                            task = task,
                            modifier = Modifier.animateContentSize(),
                            onTaskEdit = {
                                taskStateClass.updateSelectedTask(task)
                                taskStateClass.updateText(task.description)
                                navController.navigate("task_edit")
                            }
                        )
                    }
                }
            }
        }
    }
}