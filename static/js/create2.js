$(function(){

    $(".remove").hide()  // 初期：削除ボタン非表示
    // to sub func
    function tosub(clone){
        clone.attr("class","form-block sub")
        clone.find(".field.title").find("label").text("サブ")
        clone.find(".field.time").hide()
        clone.find(".field.sub").find("input").val("Ture")
        clone.find(".remove").show()
    };
    // to main func
    function tomain(clone){
        clone.attr("class","form-block main")
        clone.find(".field.title").find("label").text("プロセス")
        clone.find(".field.time").show()
        clone.find(".field.sub").find("input").val("False")
    };
    // 
    var Total= $("#id_process_set-TOTAL_FORMS")
    

    // action
    // main button
    $(".add-main").click(function(){
        var root= $(this).parent();
        var target= root.prev();
        var clone= target.clone(true);
        var but_clone= root.clone(true);
        clone.insertAfter(target)
        but_clone.insertAfter(target);
        // to main
        tomain(clone)
        //
        $(".form-block").each(function(i){
            $(this).attr("id","block-"+i);
            $(this).find(".field.rank").find("input").val(i)
        });
        Total.val($(".form-block").length)
        // 削除ボタンを表示
        if ($('.form-block.main').length >= 2) {
            $(".remove").show();
        };

    });

    $(".add-top-main").click(function(){
        var root= $("#block-0");
        var clone= root.clone(true);
        var but= root.next();
        var but_clone= but.clone(true);
        clone.insertBefore(root)
        but_clone.insertBefore(root);
        // to main
        tomain(clone);
        //
        $(".form-block").each(function(i){
            $(this).attr("id","block-"+i);
            $(this).find(".field.rank").find("input").val(i)
        });
        Total.val($(".form-block").length)
        // 削除ボタンを表示
        if ($('.form-block.main').length >= 2) {
            $(".remove").show();  
        };
    });

    // sub button
    $(".add-sub").click(function(){
        var root= $(this).parent();
        var target= root.prev();
        var clone= target.clone(true);
        var but_clone= root.clone(true);
        // clone
        clone.insertAfter(target)
        but_clone.insertAfter(target);
        // to sub
        tosub(clone)
        //
        $(".form-block").each(function(i){
            $(this).attr("id","block-"+i);
            $(this).find(".field.rank").find("input").val(i)
        });  
        Total.val($(".form-block").length)
    });

    $(".add-top-sub").click(function(){
        var root= $("#block-0");
        var clone= root.clone(true);
        var but= root.next();
        var but_clone= but.clone(true);
        // clone
        clone.insertBefore(root)
        but_clone.insertBefore(root);
        // to sub
        tosub(clone)
        //
        $(".form-block").each(function(i){
            $(this).attr("id","block-"+i);
            $(this).find(".field.rank").find("input").val(i)
        });
        Total.val($(".form-block").length)
    });

    // remove button
    $(".remove").click(function(){
        var root= $(this).parent();
        var but= root.next();
        but.remove()
        root.remove();
        //
        $(".form-block").each(function(i){
            $(this).attr("id","block-"+i);
            $(this).find(".field.rank").find("input").val(i)
        });
        Total.val($(".form-block").length)
        // 削除ボタンを非表示
        if ($('.form-block.main').length < 2) {
            $(".form-block.main").find(".remove").hide();
        };
    });
 
});