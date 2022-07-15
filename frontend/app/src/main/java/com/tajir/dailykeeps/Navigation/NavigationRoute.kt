package com.tajir.dailykeeps.Navigation

import android.os.Build
import androidx.annotation.RequiresApi
import androidx.compose.runtime.Composable
import androidx.navigation.compose.rememberNavController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import com.tajir.dailykeeps.ui.*

@RequiresApi(Build.VERSION_CODES.O)
@Composable
fun NavigationRoute() {
    val navController = rememberNavController()
    NavHost(navController = navController, startDestination = "login") {
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