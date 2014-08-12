<script src="http://code.jquery.com/jquery-1.7.1.min.js"></script>
<script src="//code.jquery.com/jquery-1.11.0.min.js"></script>

<script>
    $.ajax({
                    type: "GET",
                    url:"http://127.0.0.1:8000/recieveonlinelist",  // or just url: "/my-url/path/"
                    data:{'username':"nothing"},
                    dataType:"json",
                    xhrFields:{
                        withCredentials: true
                    },
                    crossDomain: true,
                    success: function(data) {
                                                //response=$.parseJSON(data)
                                               alert(data['onlinelist'][0]['username']);

                                                var output="<ul>";
                                                for (var item in data['onlinelist']) {
                                                    var user_id=data['onlinelist'][item].username;
                                                    console.log(user_id);
                                                    //console.log(user_id);
                                                    output+='<li><a href="#" onclick="chatuser(\'' + user_id + '\')" id="+user_id+"> '+ user_id +  '</a></li>';
                                                    }

                                                output+="</ul>";
                                                document.getElementById("onlineusers").innerHTML=output;
                                            },
                    error: function(xhr, textStatus, errorThrown){
                                                                    alert("Please report this error: "+errorThrown+xhr.status);
                                                                }
                    });
  
    </script>