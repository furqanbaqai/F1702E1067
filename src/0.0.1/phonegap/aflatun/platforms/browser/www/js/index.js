// Device Event Listener
// document.addEventListener("deviceready", onDeviceReady, false);
$(document).ready(function () {
    console.log('Device is ready......')
    document.addEventListener('deviceready', onDeviceReady, true);
    displayLoading();
});
// fucntion which will be triggered when device is ready
function onDeviceReady() {
    console.log('Device is all ready');    
    $.ajaxSetup({
        timeout: 7000
    });
    // Step#1: Get top 10 news            
    // getTopNews();
    getTopNewsAJAX();
    registerBackButton();
}

function getTopNewsAJAX(){
    console.log('Calling ajax function');    
    $('#content').show();
    $('#newsCont').hide();
    $('#btnBack').hide();
    $("#content").html('');    
    // alert('Calling: http://192.168.0.8/news/api/v1.0/topnews');
    $.get("http://192.168.0.17/news/api/v1.0/topnews",function(data){},"json")
        .done(function(data){
            console.log("Response received...");
             $.each(data.result, function (index, item) {
                 heading = item.heading;
                 excerpt = item.excerpt;
                 source = item.source;
                 detailURL = item.detailURL;
                 imageFileName = item.imageFileName;
                 imageURL = item.imageURL;
                 id = item.ContentHash;
                 fetchedOn = item.fetchedOn;
                 source = item.source;                 
                 var htmlStr = '<div id="div' + id + '" class="ui-body ui-body-a ui-corner-all">';
                 htmlStr += '<img src="' + imageURL + '" width="100%" height="200px" id="fnImage" />';
                 htmlStr += '<h2 id="h2' + id + '">' + heading + '</h2>';
                 htmlStr += '<p>' + excerpt + '</p>';
                 htmlStr += '<p align="right"><a id="tags" data-role="button" data-mini="true" cId="'+id+'"> display tags </a></p>';
                 htmlStr += '<p align="right" style="color:grey;font-size:12px">' + source + '&nbsp;|&nbsp;' + fetchedOn + '</p>';                                                  
                 // htmlStr += '<div style="display:none id=t+'+id+'"> Tags</div>'
                 htmlStr += '</div>';
                 
                 htmlStr += '<div style="display:none"> Tags</div>'
                 var oHtml = $.parseHTML(htmlStr);
                 $("#content").append(oHtml);
             });
             registerDisplayTags();
             $.mobile.loading("hide");
        })
        .fail(function(result){
            console.log("Call failed");
            console.log("error:" + JSON.stringify(result));
            $(home).hide();
            $(error).show();
            $(errorHd).text('Unable to connect to the backend server.'+JSON.stringify(result));
            $.mobile.loading("hide");
        })
        .always(function(){
            console.log("Always called");
        }); 
}

function registerDisplayTags(){
    $(document).on('click','#tags',function(){        
        console.log('Calling service to fetch tags.');
        console.log('Calling URL:' + "http://192.168.0.17/news/api/v1.0/entities/" + $(this).attr('cId'));
        $.get(
            "http://192.168.0.17/news/api/v1.0/entities/" + $(this).attr('cId'),
                function (data) {}, "json")
                .done(function(data){
                    console.log('Response received');                                        
                    // TODO! Iterate through the response and display all tags                    
                    $('#tagsList').html('');
                    $.each(data.result, function(index,item){
                        if(item.type != 'OTHER' & item.name != null){                            
                            $('#tagsList').append('<li><table style="width:100%;border: 0"><tr><td style="width:20px">' + getIconImage(item.type) + '</td><td>' + item.name + '</td></tr></table> </li>');
                        }                        
                    });                                        
                    $('#content').hide();                                        
                    $('#newsCont').show();
                    $('#tagsList').listview('refresh');
                    $('#btnBack').show();
                })
                .fail(function(result){
                    console.log('Error recevied while fetching tags.');
                    console.log('Error detail:' + JSON.stringify(result));
                })
                .always(function(){
                    console.log('Service called for fetching tags');
                });        
    });
}

function registerBackButton(){
    $(document).on('click', '#btnBack', function () {
        $('#content').show();
        $('#newsCont').hide();
        $('#btnBack').hide();
    });
}


function displayLoading(){
    var $this = $(this),
        theme = $this.jqmData("theme") || $.mobile.loader.prototype.options.theme,
        msgText = $this.jqmData("msgtext") || $.mobile.loader.prototype.options.text,
        textVisible = $this.jqmData("textvisible") || $.mobile.loader.prototype.options.textVisible,
        textonly = !!$this.jqmData("textonly");
    html = $this.jqmData("html") || "";
    $.mobile.loading("show", {
        text: msgText,
        textVisible: textVisible,
        theme: theme,
        textonly: textonly,
        html: html
    });
}

function getIconImage(tagType){
    switch(tagType){
        case 'PERSON':
            return '<img src="img/cf6e3c9d010d2af3871e72e49b85cbf6.png"  width="12px" height="12px"/>';
        case 'EVENT':
            return '<img src="img/2018032716180638.png"  width="12px" height="12px"/>';
        case 'LOCATION':        
            return '<img src="img/location-512.png"  width="12px" height="12px"/>';
        case 'ORGANIZATION':
            return '<img src="img/house_icon-01.png"  width="12px" height="12px"/>';
        case 'WORK_OF_ART':
            return '<img src="img/Paint.png"  width="12px" height="12px"/>';
        case 'CONSUMER_GOOD':
            return '<img src="img/atos-icon-consumer-packaged-goods.png"  width="12px" height="12px"/>';
        default:
            return '';

    }
}