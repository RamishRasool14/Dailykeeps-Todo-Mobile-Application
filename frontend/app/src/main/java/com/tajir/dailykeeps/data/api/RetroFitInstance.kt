package com.tajir.dailykeeps.data.api

import com.tajir.dailykeeps.data.api.interfeces.Interface
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

const val BASE_URL_LIVE = "https://ramish-todo.herokuapp.com/"

class RetrofitInstance {

    private val retrofit by lazy {
        Retrofit.Builder()
            .baseUrl(BASE_URL_LIVE)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
    }

    val Api: Interface by lazy {
        retrofit.create(Interface::class.java)
    }

}