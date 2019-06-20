const REQUEST_PROFILE = "requestProfile";
const REQUEST_PAY = "requestPay";
const REQUEST_PROOF = "requestProof";

const ON_PROFILE = "onProfile";
const ON_PAY = "onPay";
const ON_PROOF = "onProof";
const ON_ERROR = "onCallNewPayError";
const NEWPAY_AGENT = "NewPay";

function connectWebViewJavascriptBridge(callback) {
    if (window.WebViewJavascriptBridge) {
        callback(WebViewJavascriptBridge)
    } else {
        console.log("start init");
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
    console.log("init jsbridge");
    console.log(JSON.stringify(bridge));
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
    bridge.registerHandler(ON_PAY, function (response, responseCallback) {
        let url = "/receive/pay/";
        $.ajax({
            url: url,
            async: true,
            type: 'post',
            data: response,
            success: function (res) {
                console.log(JSON.stringify(res));
                if(res.error_code == 1) {
                    window.location.href = "/placeorder/"
                }
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
