
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

let starRecipe = function (recipeId) {
    let url = "/stared/" + recipeId;
    // window.open("/delete/" + recipeId, "_self");
    $.ajax({
        url: url,
        type: 'get',
        data: {
            csrftoken: Cookies.get("csrftoken"),
        },
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": Cookies.get("csrftoken"),
        },
        xhrFields: {
            withCredentials: true
        },
        
    }).done(function(data){
        console.log(data)
        if (data == 'success') {
            alert('ваш голос будет учтен');
            $('.main-btn').addClass('liked-btn');
        }
        else if (data == 'voted') {
            alert('вы уже голосовали');
        }
        else if (data == 'fail')  {
            alert('что-то пошло не так')
        }
        // window.open("/", "_self");
        // win.document.write(data);
    }).
    fail(function(data){
        console.log('fail');
        alert('что-то пошло не так')
    });

}


function ConfirmDialog(recLink) {
  $('<div></div>').appendTo('body')
    .html('<div><h6>' + 'Удалить рецепт' + '?</h6></div>')
    .dialog({
      modal: true,
      title: 'подтвердите',
      zIndex: 10000,
      autoOpen: true,
      width: 'auto',
      resizable: false,
      buttons: {
        ДА: function() {
            let recipeId = $(recLink).data('rec_id');
            let url = "/delete/" + recipeId;
            // window.open("/delete/" + recipeId, "_self");
            $.ajax({
                url: url,
                type: 'get',
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
                window.open("/", "_self");
                // win.document.write(data);
              
                
            }).
            fail(function(data){
                console.log('fail');
                console.log(data);
            });


          $(this).dialog("close");
        },
        НЕТ: function() {
          $(this).dialog("close");
        }
      },
      close: function(event, ui) {
        $(this).remove();
      }
    });
};
