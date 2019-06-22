const REQUEST_PROFILE = "requestProfile";
const REQUEST_PAY = "requestPay";
const REQUEST_PROOF = "requestProof";

const ON_PROFILE = "onProfile";
const ON_PAY = "onPay";
const ON_PROOF = "onProof";
const ON_ERROR = "onCallNewPayError";
const NEWPAY_AGENT = "NewPay";


var bridge = {
    default: this,
    call: function (b, a, c) {
        var e = "";
        "function" == typeof a && (c = a, a = {});
        a = {
            data: void 0 === a ? null : a
        };
        if ("function" == typeof c) {
            var g = "dscb" + window.dscb++;
            window[g] = c;
            a._dscbstub = g
        }
        a = JSON.stringify(a);
        if (window._dsbridge) e = _dsbridge.call(b, a);
        else if (window._dswk || -1 != navigator.userAgent.indexOf("_dsbridge")) e = prompt("_dsbridge=" + b, a);
        return JSON.parse(e || "{}").data
    },
    register: function (b, a, c) {
        c = c ? window._dsaf : window._dsf;
        window._dsInit || (window._dsInit = !0, setTimeout(function () {
                bridge.call("_dsb.dsinit")
            },
            0));
        "object" == typeof a ? c._obs[b] = a : c[b] = a
    },
    registerAsyn: function (b, a) {
        this.register(b, a, !0)
    },
    hasNativeMethod: function (b, a) {
        return this.call("_dsb.hasNativeMethod", {
            name: b,
            type: a || "all"
        })
    },
    disableJavascriptDialogBlock: function (b) {
        this.call("_dsb.disableJavascriptDialogBlock", {
            disable: !1 !== b
        })
    }
};
! function () {
    if (!window._dsf) {
        var b = {
                _dsf: {
                    _obs: {}
                },
                _dsaf: {
                    _obs: {}
                },
                dscb: 0,
                dsBridge: bridge,
                close: function () {
                    bridge.call("_dsb.closePage")
                },
                _handleMessageFromNative: function (a) {
                    var e = JSON.parse(a.data),
                        b = {
                            id: a.callbackId,
                            complete: !0
                        },
                        c = this._dsf[a.method],
                        d = this._dsaf[a.method],
                        h = function (a, c) {
                            b.data = a.apply(c, e);
                            bridge.call("_dsb.returnValue", b)
                        },
                        k = function (a, c) {
                            e.push(function (a, c) {
                                b.data = a;
                                b.complete = !1 !== c;
                                bridge.call("_dsb.returnValue", b)
                            });
                            a.apply(c, e)
                        };
                    if (c) h(c, this._dsf);
                    else if (d) k(d, this._dsaf);
                    else if (c = a.method.split("."), !(2 > c.length)) {
                        a = c.pop();
                        var c = c.join("."),
                            d = this._dsf._obs,
                            d = d[c] || {},
                            f = d[a];
                        f && "function" == typeof f ? h(f, d) : (d = this._dsaf._obs, d = d[c] || {}, (f = d[a]) &&
                            "function" == typeof f && k(f, d))
                    }
                }
            },
            a;
        for (a in b) window[a] = b[a];
        bridge.register("_hasJavascriptMethod", function (a, b) {
            b = a.split(".");
            if (2 > b.length) return !(!_dsf[b] && !_dsaf[b]);
            a = b.pop();
            b = b.join(".");
            return (b = _dsf._obs[b] || _dsaf._obs[b]) && !!b[a]
        })
    }
}();
var dsBridge = bridge;
dsBridge.registerAsyn(ON_PROFILE, function (profile) {
    let url = "/post/profile/";
    console.log(JSON.stringify(profile));
    $.ajax({
        url: url,
        async: true,
        type: 'post',
        data: profile,
        success: function (res) {
            console.log(JSON.stringify(res));
            if(res.error_code == 1) {
                window.location.href = "/user"
            }
        }
    })
});
dsBridge.registerAsyn(ON_PAY, function (pay_info) {
    let url = "/receive/pay/";
    $.ajax({
        url: url,
        async: true,
        type: 'post',
        data: pay_info,
        success: function (res) {
            console.log(JSON.stringify(res));
            if(res.error_code == 1) {
                window.location.href = "/placeorder/"
            }
        }
    })
});
dsBridge.registerAsyn(ON_PROOF, function (proof_info) {
    let url = "/receive/proof/";
    $.ajax({
        url: url,
        async: true,
        type: 'post',
        data: proof_info,
        success: function (res) {
            console.log(res);
            $('#tip').val("success")
        }
    })
});
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
                // window.WebViewJavascriptBridge.callHandler(
                //     REQUEST_PROFILE, params
                // )
                dsBridge.call(REQUEST_PROFILE, params, function (res) {
                    console.log("call success")
                })
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
                // window.WebViewJavascriptBridge.callHandler(
                //     REQUEST_PAY, params
                // )
                dsBridge.call(REQUEST_PAY, params, function (res) {
                    console.log("call success")
                });
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
                // window.WebViewJavascriptBridge.callHandler(
                //     REQUEST_PROOF, params
                // )
                dsBridge.call(REQUEST_PROOF, params, function (res) {
                    console.log("call success")
                });
            }
        }
    });
}
