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
