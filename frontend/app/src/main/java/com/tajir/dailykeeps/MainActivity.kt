package com.tajir.dailykeeps

import android.content.Context
import android.os.Build
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.viewModels
import androidx.annotation.RequiresApi
import androidx.compose.material.MaterialTheme
import androidx.compose.runtime.CompositionLocalProvider
import com.tajir.dailykeeps.Navigation.NavigationRoute
import com.tajir.dailykeeps.ui.session.Session
import com.tajir.dailykeeps.viewmodels.*


class MainActivity : ComponentActivity() {
    private val authState by viewModels<AuthenticationViewModel>()
    private val taskState by viewModels<TaskViewModel>{
        MyViewModelFactory(
            application,
            this.applicationContext
        )
    }

    @RequiresApi(Build.VERSION_CODES.O)
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        setContent {
            CompositionLocalProvider(
                AuthState provides authState,
                TaskState provides taskState,
            )
            {
                MaterialTheme {
                    NavigationRoute(this.applicationContext)
                }
            }
        }
    }
}
