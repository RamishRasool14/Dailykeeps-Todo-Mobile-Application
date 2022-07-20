package com.tajir.dailykeeps.data.api

import com.tajir.dailykeeps.data.api.interfeces.Interface
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

val BASE_URL_LIVE = "https://ramish-todoapp-dot-hum-retail-dev.uc.r.appspot.com"
val BASE_URL_LOCAL = "http://192.168.2.99:80"

class RetrofitInstance {

    private val retrofit by lazy {
        Retrofit.Builder()
            .baseUrl(BASE_URL_LOCAL)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
    }

    val Api: Interface by lazy {
        retrofit.create(Interface::class.java)
    }

}