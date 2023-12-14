
let myRecipes = function () {
    let url = "/";
    // Cookies.set("csrftoken", Cookies.get("csrftoken"));

    $.ajax({
        url: url,
        type: 'post',
        data: {
            csrftoken: Cookies.get("csrftoken"),
            'my_recipes': true,
        },
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": Cookies.get("csrftoken"),
        },
        xhrFields: {
            withCredentials: true
        },
        
    }).done(function(data){
        console.log('success')
        var win = window.open("", "_self");
        win.document.write(data);
      
        
    }).
    fail(function(data){
        console.log('fail');
        console.log(data);
    });
}