package com.tajir.dailykeeps.ui.components

import android.os.Build
import androidx.annotation.RequiresApi
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material.icons.filled.MoreVert
import androidx.compose.material.icons.filled.PanoramaFishEye
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.SpanStyle
import androidx.compose.ui.text.buildAnnotatedString
import androidx.compose.ui.text.style.TextDecoration
import androidx.compose.ui.text.withStyle
import androidx.compose.ui.unit.dp
import com.tajir.dailykeeps.data.api.interfeces.models.Task
import com.tajir.dailykeeps.viewmodels.TaskState

@RequiresApi(Build.VERSION_CODES.O)
@Composable
fun TaskCard(
    task: Task,
    modifier: Modifier,
    onTaskEdit: () -> Unit
) {
    var expanded by remember { mutableStateOf(false) }

    val taskStateClass = TaskState.current
    val taskState = taskStateClass.taskState.collectAsState().value
    taskStateClass.updateSelectedTask(task)

    Row(modifier = modifier) {
        Card(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 7.dp, vertical = 7.dp)
                .clickable {
                    onTaskEdit()
                },
            elevation = 10.dp,
            shape = RoundedCornerShape(5.dp)
        ) {
            Row(
                horizontalArrangement = Arrangement.Start,
                verticalAlignment = Alignment.CenterVertically
            ) {
                IconButton(
                    onClick = {
                        taskStateClass.editTaskStatus(task)
                    }
                ) {
                    Icon(
                        imageVector = Icons.Default.PanoramaFishEye,
                        contentDescription = "Status",
                        tint = if(task.done) Color.Green else Color.Red
                    )
                }

                Column(
                    modifier = Modifier.padding(15.dp)
                ) {
                    Text(
                        buildAnnotatedString {
                            withStyle(
                                style = SpanStyle(
                                    textDecoration = if(!task.done) TextDecoration.None else TextDecoration.LineThrough
                                )
                            ) {
                                append(task.description.take(30))
                            }
                        }
                    )
                }

                Box(modifier = Modifier.fillMaxSize().wrapContentSize(Alignment.TopEnd)) {
                    IconButton(onClick = { taskStateClass.deleteTask(task.id) }) {
                        Icon(imageVector =  Icons.Default.Delete, contentDescription = "Localized description", tint = Color.Red)
                    }
                }

            }
        }
    }
}