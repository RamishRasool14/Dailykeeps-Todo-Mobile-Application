package com.tajir.dailykeeps.ui

import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.material.Button
import androidx.compose.material.CircularProgressIndicator
import androidx.compose.material.Text
import androidx.compose.material.TextButton
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.navigation.NavController
import com.tajir.dailykeeps.ui.components.InputField
import com.tajir.dailykeeps.ui.components.PasswordField
import com.tajir.dailykeeps.viewmodels.AuthState
import com.tajir.dailykeeps.R
import com.tajir.dailykeeps.viewmodels.TaskState

@Composable
fun LoginScreen(
    navController: NavController
) {

    val authStateClass = AuthState.current
    val loginState = AuthState.current.loginState.collectAsState().value
    val taskClass = TaskState.current

        Column(
            modifier = Modifier.fillMaxSize(),
            verticalArrangement = Arrangement.Center,
            horizontalAlignment = Alignment.CenterHorizontally,
        ) {
            Text(
                text = loginState.status,
                fontWeight = FontWeight.Bold,
                fontSize = 20.sp,
                modifier = Modifier.padding(20.dp)
            )
            Image(painterResource(R.drawable.logo),"content description")

            Text(
                text = "Log In",
                fontSize = 30.sp,
                fontWeight = FontWeight.Bold,
                modifier = Modifier.padding(20.dp)
            )
            InputField(
                inputValue = loginState.email,
                onValueChanged = {
                    authStateClass.updateEmailLogin(it)
                },
                label = "Email"
            )

            PasswordField(
                inputValue = loginState.password,
                onValueChanged = {
                    authStateClass.updatePasswordLogin(it)
                },
                label = "Password",
            )

            Button(
                modifier = Modifier.padding(10.dp),
                onClick = {
                    authStateClass.login()
                }
            ) {
                Text(text = "Login", fontSize = 20.sp)
            }

            TextButton(
                onClick = {
                    navController.navigate("register")
                }
            ) {
                Text(text = "Need an account?", fontSize = 15.sp)
            }

            Text(
                text = loginState.err,
                fontWeight = FontWeight.Bold,
                fontSize = 15.sp,
                color = androidx.compose.ui.graphics.Color.Red
            )

            if (loginState.loading) {
                Box(
                    contentAlignment = Alignment.Center,
                    modifier = Modifier.background(color = androidx.compose.ui.graphics.Color.White)
                ) {
                    CircularProgressIndicator()
                }
            }
        }

    if (loginState.token != "")
    {
        taskClass.updateToken(loginState.token)
        taskClass.getTask()
        navController.navigate("main")
        authStateClass.updateToken("")
    }
}