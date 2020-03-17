function h5login() {
    let url = "/request/login/h5/";
    $.ajax({
        url: url,
        async: true,
        type: 'post',
        success: function (res) {
            console.log(JSON.stringify(res));
            if(res.error_code === 1) {
                let params = res.result;
                if(hep) {
                    hep.auth.login(params, function (response) {
                        if(response.status_code === 200) {
                            var profile = response.result;
                            console.log(JSON.stringify(profile));
                            let url = "/post/profile/";
                            $.post(url, profile, function (res) {
                                console.log(JSON.stringify(res));
                                if(res.error_code === 1) {
                                    window.location.href = "/user"
                                }
                            }, "json")
                        } else {
                            alert(response.message);
                        }
                    });
                }else {
                    alert("hep is not inject");
                }
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
            if(res.error_code === 1) {
                if(hep) {
                    let params = res.result;
                    hep.pay.order(params, function (response) {
                        if(response.status_code === 200) {
                            var pay_info = response.result;
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
                            });
                        } else {
                            alert(response.message);
                        }
                    })
                } else {
                    alert("hep is not inject");
                }
            }
        }
    });
}
function requestSignMessage() {
    let url = "/get/client/sign/message/";
    $.ajax({
        url: url,
        async: true,
        type: 'post',
        data: {'message': $("#input-sign-message").val()},
        success: function (res) {
            if(res.error_code === 1) {
                if(hep) {
                    let params = res.result;
                    hep.sign.message(params, function(response) {
                        alert("签名结果:" + response.result);
                    });
                } else {
                    alert("hep is not inject");
                }
            }
        }
    });
}

function requestSignTransaction() {
    let url = "/get/client/sign/transaction/";
    $.ajax({
        url: url,
        async: true,
        type: 'post',
        data: {'amount': $("#input-amount").val(),
                'from': $("#input-from-address").val(),
                'to': $('#input-to-address').val(),
                'data': $('#input-data').val(),
                'gas_limit': $('#input-gas-limit').val(),
                'gas_price': $('#input-gas-price').val(),
                'transaction_count': $('#input-transaction-count').val()
                },
        success: function (res) {
            if(res.error_code === 1) {
                if(hep) {
                    let params = res.result;
                    hep.sign.transaction(params, function(response) {
                        alert("签署交易结果:" + response.result);
                    });
                } else {
                    alert("hep is not inject");
                }
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
            if(res.error_code === 1) {
                if(hep) {
                    let params = res.result;
                    hep.proof.submit(params, function(response) {
                        if(response.status_code === 200) {
                            var proof_info = response.result;
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
                        } else {
                            alert(response.message);
                        }
                    });
                } else {
                    alert("hep is not inject");
                }
            }
        }
    });
}
