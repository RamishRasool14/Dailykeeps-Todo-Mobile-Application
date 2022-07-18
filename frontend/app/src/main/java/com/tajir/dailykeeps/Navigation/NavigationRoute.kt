package com.tajir.dailykeeps.Navigation

import android.content.Context
import android.os.Build
import androidx.annotation.RequiresApi
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.navigation.compose.rememberNavController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import com.tajir.dailykeeps.ui.*
import com.tajir.dailykeeps.ui.session.Session
import com.tajir.dailykeeps.viewmodels.TaskState

@RequiresApi(Build.VERSION_CODES.O)
@Composable
fun NavigationRoute(context: Context) {
    val navController = rememberNavController()
    var session: Session = Session(context)
    var startDest: String = "login"

    val taskStateClass = TaskState.current
    if (session.getusename().isNotEmpty())
    {
        startDest = "main"
        taskStateClass.updateToken(session.getusename())
        taskStateClass.getTask()

    }
    NavHost(navController = navController, startDestination = startDest) {
        composable("login") {
            LoginScreen(navController = navController)
        }

        composable("register") {
            RegisterScreen(navController = navController)
        }

        composable("main") {
            MainScreen(navController = navController)
        }

        composable("task_edit") {
            TaskScreen(navController = navController)
        }
    }
}