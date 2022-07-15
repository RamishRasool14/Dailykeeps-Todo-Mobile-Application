package com.tajir.dailykeeps

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.viewModels
import androidx.compose.material.MaterialTheme
import androidx.compose.runtime.CompositionLocalProvider
import com.tajir.dailykeeps.Navigation.NavigationRoute
import com.tajir.dailykeeps.viewmodels.AuthState
import com.tajir.dailykeeps.viewmodels.AuthenticationViewModel
import com.tajir.dailykeeps.viewmodels.TaskState
import com.tajir.dailykeeps.viewmodels.TaskViewModel

class MainActivity : ComponentActivity() {
    private val authState by viewModels<AuthenticationViewModel>()
    private val taskState by viewModels<TaskViewModel>()


    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            CompositionLocalProvider(
                AuthState provides authState,
                TaskState provides taskState,
            ) {
                MaterialTheme {
                    NavigationRoute()
                }
            }
        }
    }
}
