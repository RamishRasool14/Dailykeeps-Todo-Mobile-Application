package com.tajir.dailykeeps.viewmodels

import android.app.Application
import android.content.Context
import androidx.compose.runtime.compositionLocalOf
import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewModelScope
import com.tajir.dailykeeps.data.StateModels.LoginState
import com.tajir.dailykeeps.data.StateModels.RegisterState
import com.tajir.dailykeeps.data.api.RetrofitInstance
import com.tajir.dailykeeps.data.api.interfeces.models.Login
import com.tajir.dailykeeps.data.api.interfeces.models.LoginResponse
import com.tajir.dailykeeps.data.api.interfeces.models.Register
import com.tajir.dailykeeps.data.api.interfeces.models.RegisterResponse
import com.tajir.dailykeeps.ui.session.Session
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.launch
import retrofit2.Response

class AuthenticationViewModel() : ViewModel() {
    val loginState = MutableStateFlow(LoginState())
    val registerState = MutableStateFlow(RegisterState())

    fun updateEmailLogin(email : String) {
        loginState.value = loginState.value.copy(
            email = email
        )
    }

    fun updateToken(token: String){
        loginState.value = loginState.value.copy(
            token = token
        )
    }

    fun setLoadingLogin(loading : Boolean) {
        loginState.value = loginState.value.copy(
            loading = loading
        )
    }

    fun updatePasswordLogin(password : String) {
        loginState.value = loginState.value.copy(
            password = password
        )
    }

    fun setErrLogin(err : String) {
        loginState.value = loginState.value.copy(
            err = err
        )
    }

    fun clearErrLogin() {
        loginState.value = loginState.value.copy(
            err = ""
        )
    }

    fun updateEmailRegister(email : String) {
        registerState.value = registerState.value.copy(
            email = email
        )
    }

    fun updateFirstNameRegister(first_name : String) {
        registerState.value = registerState.value.copy(first_name = first_name)
    }

    fun updateLastNameRegister(last_name : String) {
        registerState.value = registerState.value.copy(last_name = last_name)
    }

    fun updatePasswordRegister(password : String) {
        registerState.value = registerState.value.copy(
            password = password
        )
    }

    fun updateRegisterResponse(response : Response<RegisterResponse>) {
        registerState.value = registerState.value.copy(
            register_response = response
        )
    }

    fun updateLoginResponse(response : Response<LoginResponse>) {
        loginState.value = loginState.value.copy(
            login_response = response
        )
        loginState.value.updateToken()
    }

    fun setLoadingRegister(loading : Boolean) {
        registerState.value = registerState.value.copy(
            loading = loading
        )
    }

    fun setErrRegister(err : String) {
        registerState.value = registerState.value.copy(
            err = err
        )
    }

    fun clearErrRegister() {
        registerState.value = registerState.value.copy(
            err = ""
        )
    }

    fun setStatus(status : String) {
        loginState.value = loginState.value.copy(
            status = status
        )
    }

    fun clearStatus(){
        loginState.value = loginState.value.copy(
            status = ""
        )
    }

    fun process()
    {
        if (loginState.value.login_response?.body()?.description == "failed to log in user" )
        {
            setStatus("Invalid email or password")
        }
        if (registerState.value.register_response?.body()?.description == "successfully registered user" )
        {
            setStatus("User registered successfully")
        }

    }

    fun register() {
        clearErrRegister()
        if (registerState.value.first_name == "")
        {
            setErrRegister("first name not found")
            return
        }
        if (registerState.value.last_name == "")
        {
            setErrRegister("last name not found")
            return
        }
        if (registerState.value.email == "")
        {
            setErrRegister("email not found")
            return
        }
        if (registerState.value.password == "")
        {
            setErrRegister("password not found")
            return
        }

        setLoadingRegister(true)
        viewModelScope.launch {
            val data = Register(
                first_name = registerState.value.first_name,
                last_name = registerState.value.last_name,
                email = registerState.value.email,
                password = registerState.value.password
            )

            try {
                val res = RetrofitInstance().Api.register(data)
                setLoadingRegister(false)
                updateRegisterResponse(res)
                process()
            } catch(e : Exception) {
                setErrRegister("Check your internet connection.")
                setLoadingRegister(false)
            }
        }

        updateEmailRegister("")
        updateFirstNameRegister("")
        updateLastNameRegister("")
        updatePasswordRegister("")

    }

    fun login() {
        clearErrLogin()
        if (loginState.value.email == "")
        {
            setErrLogin("email not found")
            return
        }
        if (loginState.value.password == "")
        {
            setErrLogin("password not found")
            return
        }
        setLoadingLogin(true)
        viewModelScope.launch {
            val data = Login(
                email = loginState.value.email,
                password = loginState.value.password
            )

            try {
                val res = RetrofitInstance().Api.login(data)
                setLoadingLogin(false)
                updateLoginResponse(res)
                process()

            } catch(e : Exception) {
                setErrLogin("Check your internet connection.")
                setLoadingLogin(false)
            }
        }
        updatePasswordLogin("")
        updateEmailLogin("")
    }

}

val AuthState by lazy {
    compositionLocalOf<AuthenticationViewModel> {
        error("Authentication Context not found.")
    }
}
