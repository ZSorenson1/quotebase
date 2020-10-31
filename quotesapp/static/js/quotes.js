$(document).ready(function(){
    $(document.getElementsByName('addQuote')).submit(function(e){
            e.preventDefault();
            $.ajax({
                url: "/quotes/create",
                method: 'post',
                data: $(this).serialize(),
                success: function(serverResponse){
                    $('.quotes').html(serverResponse)
                }
            });
        });
    

    $(document).on('click', '.Close', function(e) {
        var catid = $(this).attr("data-catid");
        $('.edit'+catid).html('');
    })

    $(document).on('click', '.edit', function(e){
        e.preventDefault();
        var catid = $(this).attr("data-catid");
        $.ajax({
            url: "/quotes/edit/"+catid,
            method: 'get',
            data: '',
            success: function(serverResponse){
                $('.edit'+catid).html(serverResponse)
            }
        });
    });

    $(document).on('click', '.delete', function(e){
        e.preventDefault();
        var catid = $(this).attr("data-catid");
        $.ajax({
            url: "/quotes/delete/"+catid,
            method: 'get',
            data: '',
            success: function(serverResponse){
                $('.allQuotes').html(serverResponse)
            }
        });
    });

    $(document).on('submit', '.editform', function(e){
        e.preventDefault();
        var catid = $(this).attr("data-catid");
        $.ajax({
            url: "/quotes/edit/"+catid+"/submit",
            method: 'post',
            data: $(this).serialize(),
            success: function(serverResponse){
                $('.allQuotes').html(serverResponse)
            }
        });
    });

    $(document).on('submit', '.addFavorite', function(e){
        e.preventDefault();
        var catid = $(this).attr("data-catid");
        $.ajax({
            url: "/quotes/addfavorite/"+catid,
            method: 'post',
            data: $(this).serialize(),
            success: function(serverResponse){
                $('.allQuotes').html(serverResponse)
            }
        });
    });

    $(document).on('submit', '.removeFavorite', function(e){
        e.preventDefault();
        var catid = $(this).attr("data-catid");
        $.ajax({
            
            url: "/quotes/removefavorite/"+catid,
            method: 'post',
            data: $(this).serialize(),
            success: function(serverResponse){
                $('.allQuotes').html(serverResponse)
            }
        });
    });

    $(document).on('click', '.user', function(e){
        e.preventDefault();
        var catid = $(this).attr("data-catid");
        $.ajax({
            
            url: "/users/"+catid,
            method: 'get',
            data: '',
            success: function(serverResponse){
                $('.body').html(serverResponse)
            }
        });
    });
    $(document).on('click', '.back', function(e){
        e.preventDefault();
        $.ajax({
            url: "/back",
            method: 'get',
            data: '',
            success: function(serverResponse){
                $('.body').html(serverResponse)
            }
        });
    });
});