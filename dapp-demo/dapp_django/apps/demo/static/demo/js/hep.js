const REQUEST_PROFILE = "requestProfile";
const REQUEST_PAY = "requestPay";
const REQUEST_PROOF = "requestProof";

const ON_PROFILE = "onProfile";
const ON_PAY = "onPay";
const ON_PROOF = "onProof";
const ON_ERROR = "onCallNewPayError";

function connectWebViewJavascriptBridge(callback) {
    if (window.WebViewJavascriptBridge) {
        callback(WebViewJavascriptBridge)
    } else {
        document.addEventListener(
            'WebViewJavascriptBridgeReady'
            , function() {
                callback(WebViewJavascriptBridge)
            },
            false
        );
    }
}

connectWebViewJavascriptBridge(function(bridge) {
    bridge.init(function(message, responseCallback) {
        console.log('JS got a message', message);
    });
    bridge.registerHandler(ON_PROFILE, function (data, responseCallback) {
        let url = "/post/profile/";
        $.ajax({
            url: url,
            async: true,
            type: 'post',
            data: data,
            success: function (res) {
                if(res.error_code == 1) {
                    window.location.href = "/user"
                }
            }
        })
    });
    bridge.registerHandler(ON_PAY, function (data, responseCallback) {
        let url = "/receive/pay/";
        console.log(window.sessionStorage.getItem('pay_id'));
        $.ajax({
            url: url,
            async: true,
            type: 'post',
            data: {'txid': data},
            success: function (res) {
                console.log(res);
            }
        })
    });
    bridge.registerHandler(ON_PROOF, function (data, responseCallback) {
        let url = "/receive/proof/";
        $.ajax({
            url: url,
            async: true,
            type: 'post',
            data: data,
            success: function (res) {
                console.log(res);
                $('#tip').val("success")
            }
        })
    });
    bridge.registerHandler(ON_ERROR, function (data, responseCallback) {
        console.log("on error:" + data);

    });
});

function h5login() {
    let url = "/request/login/h5/";
    $.ajax({
        url: url,
        async: true,
        type: 'post',
        success: function (res) {
            console.log(JSON.stringify(res));
            if(res.error_code == 1) {
                console.log(res);
                let params = res.result;
                window.WebViewJavascriptBridge.callHandler(
                    REQUEST_PROFILE, params
                )
            }
        }
    });
}

function h5pay() {
    let url = "/request/pay/h5/";
    $.ajax({
        url: url,
        async: true,
        type: 'post',
        data: {'order_number': 'orderNumber'},
        success: function (res) {
            console.log(JSON.stringify(res));
            if(res.error_code == 1) {
                console.log(res);
                let params = res.result;
                window.WebViewJavascriptBridge.callHandler(
                    REQUEST_PAY, params
                )
            }
        }
    });
}

function h5proof() {
    let url = "/request/proof/h5/";
    $.ajax({
        url: url,
        async: true,
        type: 'post',
        data: {'order_number': 'orderNumber'},
        success: function (res) {
            console.log(JSON.stringify(res));
            if(res.error_code == 1) {
                console.log(res);
                let params = res.result;
                window.WebViewJavascriptBridge.callHandler(
                    REQUEST_PROOF, params
                )
            }
        }
    });
}