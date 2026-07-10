package com.newsapp.mobile

import android.annotation.SuppressLint
import android.content.Context
import android.graphics.Bitmap
import android.os.Bundle
import android.view.View
import android.webkit.WebChromeClient
import android.webkit.WebResourceRequest
import android.webkit.WebSettings
import android.webkit.WebView
import android.webkit.WebViewClient
import android.widget.Button
import android.widget.ProgressBar
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import com.google.android.material.textfield.TextInputEditText

class MainActivity : AppCompatActivity() {
    private lateinit var configContainer: View
    private lateinit var webView: WebView
    private lateinit var progressBar: ProgressBar
    private lateinit var errorText: TextView
    private lateinit var urlInput: TextInputEditText
    private lateinit var saveButton: Button
    private lateinit var changeServerButton: Button

    private val prefs by lazy { getSharedPreferences("news_app_prefs", Context.MODE_PRIVATE) }

    @SuppressLint("SetJavaScriptEnabled")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        configContainer = findViewById(R.id.configContainer)
        webView = findViewById(R.id.webView)
        progressBar = findViewById(R.id.progressBar)
        errorText = findViewById(R.id.errorText)
        urlInput = findViewById(R.id.urlInput)
        saveButton = findViewById(R.id.saveButton)
        changeServerButton = findViewById(R.id.changeServerButton)

        webView.settings.javaScriptEnabled = true
        webView.settings.domStorageEnabled = true
        webView.settings.cacheMode = WebSettings.LOAD_DEFAULT
        webView.settings.mixedContentMode = WebSettings.MIXED_CONTENT_COMPATIBILITY_MODE
        webView.settings.loadsImagesAutomatically = true
        webView.settings.setSupportZoom(false)

        webView.webChromeClient = object : WebChromeClient() {
            override fun onProgressChanged(view: WebView?, newProgress: Int) {
                progressBar.progress = newProgress
                progressBar.visibility = if (newProgress < 100) View.VISIBLE else View.GONE
            }
        }

        webView.webViewClient = object : WebViewClient() {
            override fun onPageStarted(view: WebView?, url: String?, favicon: Bitmap?) {
                progressBar.visibility = View.VISIBLE
                errorText.visibility = View.GONE
            }

            override fun onReceivedError(
                view: WebView?,
                request: WebResourceRequest?,
                error: android.webkit.WebResourceError?
            ) {
                if (request?.isForMainFrame == true) {
                    showError()
                }
            }
        }

        val initialUrl = savedUrl().ifBlank { BuildConfig.NEWS_APP_URL }
        urlInput.setText(initialUrl)

        saveButton.setOnClickListener {
            val normalizedUrl = normalizeUrl(urlInput.text?.toString().orEmpty())
            if (normalizedUrl == null) {
                showConfig(getString(R.string.invalid_url_message))
            } else {
                prefs.edit().putString(PREF_SERVER_URL, normalizedUrl).apply()
                loadNewsApp(normalizedUrl)
            }
        }

        changeServerButton.setOnClickListener {
            showConfig()
        }

        if (initialUrl.isBlank() || initialUrl.contains("YOUR-DEPLOYED-URL")) {
            showConfig(getString(R.string.missing_url_message))
        } else {
            loadNewsApp(initialUrl)
        }
    }

    private fun loadNewsApp(url: String) {
        configContainer.visibility = View.GONE
        webView.visibility = View.VISIBLE
        changeServerButton.visibility = View.VISIBLE
        progressBar.visibility = View.VISIBLE
        errorText.visibility = View.GONE
        webView.loadUrl(url)
    }

    private fun showError() {
        progressBar.visibility = View.GONE
        webView.visibility = View.GONE
        showConfig(getString(R.string.load_error_message))
    }

    private fun showConfig(message: String? = null) {
        configContainer.visibility = View.VISIBLE
        webView.visibility = View.GONE
        changeServerButton.visibility = View.GONE
        progressBar.visibility = View.GONE
        if (message.isNullOrBlank()) {
            errorText.visibility = View.GONE
        } else {
            errorText.visibility = View.VISIBLE
            errorText.text = message
        }
    }

    private fun savedUrl(): String = prefs.getString(PREF_SERVER_URL, "")?.trim().orEmpty()

    private fun normalizeUrl(rawUrl: String): String? {
        val trimmed = rawUrl.trim()
        if (trimmed.isBlank()) {
            return null
        }

        val candidate = if (trimmed.endsWith("/")) trimmed else "$trimmed/"
        return if (candidate.startsWith("http://") || candidate.startsWith("https://")) {
            candidate
        } else {
            null
        }
    }

    override fun onBackPressed() {
        if (::webView.isInitialized && webView.canGoBack()) {
            webView.goBack()
        } else {
            super.onBackPressed()
        }
    }

    companion object {
        private const val PREF_SERVER_URL = "server_url"
    }
}
