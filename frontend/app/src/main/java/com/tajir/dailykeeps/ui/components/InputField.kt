package com.tajir.dailykeeps.ui.components

import androidx.compose.foundation.ScrollState
import androidx.compose.foundation.gestures.scrollable
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.*
import androidx.compose.material.Text
import androidx.compose.material.TextField
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

@Composable
fun InputField(
    inputValue : String,
    onValueChanged : (value : String) -> Unit,
    label : String,

) {
    Column(modifier = Modifier.height(85.dp).width(280.dp) ) {
        Text(text = label, fontSize = 20.sp)
        TextField(value = inputValue, onValueChange = onValueChanged)
    }
}
