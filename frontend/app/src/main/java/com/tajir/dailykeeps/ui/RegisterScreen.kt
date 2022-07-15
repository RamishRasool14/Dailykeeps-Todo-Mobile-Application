package com.tajir.dailykeeps.ui

import android.graphics.Color
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.material.Button
import androidx.compose.material.CircularProgressIndicator
import androidx.compose.material.Text
import androidx.compose.material.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.navigation.NavController
import com.tajir.dailykeeps.R
import com.tajir.dailykeeps.ui.components.InputField
import com.tajir.dailykeeps.ui.components.PasswordField
import com.tajir.dailykeeps.viewmodels.AuthState

@Composable
fun RegisterScreen(
    navController: NavController
) {

    val authStateClass = AuthState.current
    val regState = AuthState.current.registerState.collectAsState().value

    if (regState.register_response != null)
    {
        if(regState.register_response!!.body()?.description == "successfully registered user")
        {
            regState.register_response = null
            navController.navigate("login")
        }
    }

        Column(
        modifier = Modifier.fillMaxSize(),
        verticalArrangement = Arrangement.Center,
        horizontalAlignment = Alignment.CenterHorizontally,
    ) { Image(painterResource(R.drawable.logo),"content description")
        Text(
            text = "Register Account",
            fontSize = 30.sp,
            fontWeight = FontWeight.Bold,
            modifier = Modifier.padding(40.dp)
        )
        InputField(
            inputValue = regState.first_name,
            onValueChanged = {
                authStateClass.updateFirstNameRegister(it)
            },
            label = "First Name"
        )

        InputField(
            inputValue = regState.last_name,
            onValueChanged = {
                authStateClass.updateLastNameRegister(it)
            },
            label = "Last Name"
        )

        InputField(
            inputValue = regState.email,
            onValueChanged = {
                authStateClass.updateEmailRegister(it)
            },
            label = "Email"
        )

        PasswordField(
            inputValue = regState.password,
            onValueChanged = {
                authStateClass.updatePasswordRegister(it)
            },
            label = "Password"
        )

        Button(
            modifier = Modifier.padding(10.dp),
            onClick = {
                authStateClass.register()
            }
        ) {
            Text(text = "Register", fontSize = 20.sp)
        }

        TextButton(
            onClick = {
                navController.navigate("login")
            }
        ) {
            Text(text = "Already have an account?", fontSize = 15.sp)
        }
        if (regState.loading) {
            Box(
                contentAlignment = Alignment.Center,
                modifier = Modifier.background(color = androidx.compose.ui.graphics.Color.White)
            ) {
                CircularProgressIndicator()
            }
        }

        Text(text = regState.err, fontSize = 20.sp, color = androidx.compose.ui.graphics.Color.Red)
    }

}