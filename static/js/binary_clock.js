$(document).ready(function(){
  
  $.fn.appendGridDiv = function(gridNo){
    this.each(function(){
        $(this).append("<div id='grid"+gridNo+"'></div>");
    });    
  };
  $.fn.appendGridSpan = function(gridNo){
    this.each(function(){
        $(this).append("<span id='grid"+gridNo+"'></span>");
    });    
  };
  
  function appendBlank(gridNo){
    $("#grid"+gridNo).append("<div class='blank'></div>");
  }
  
  function appendDot(idNo){
    $("#grid"+idNo.toString().charAt(0)).append("<div id='"+idNo+"' class='dot'></div>");
  }
  
 
  $.fn.fillDot = function(color){
    this.each(function(){
        $(this).removeClass('dot').addClass('dotfilled').css('background', color);
    });    
  };
  $.fn.clearDot = function(){
    this.each(function(){
        $(this).removeClass('dotfilled').addClass('dot');
    });    
  };
  
  var BinaryClock = function(oncolor, offcolor){
    var style1 = $('<style>.dotfilled { background-color:'+oncolor+'; }</style>');
    var style2 = $('<style>.dot { background-color:'+offcolor+'; }</style>');
    $('html > head').append(style1);
    $('html > head').append(style2);
  };
  
 /************BEGIN DIRECTION PROTOTYPE***********/ 
  BinaryClock.prototype.direction=function(direction){
    this.direction = direction;
    var style;
    if(direction=="topBottom"){
      for(i=1;i<9;i*=2){
        $("#bincont").appendGridDiv(i);
      }
      style=$('<style>.dot, .dotfilled, .blank { display: inline-block; }</style>');
      $('html > head').append(style);
    }
    if(direction=="bottomTop"){
      for(i=8;i>=1;i-=(i/2)){
        $("#bincont").appendGridDiv(i);
      }
      style=$('<style>.dot, .dotfilled, .blank { display: inline-block; }</style>');
      $('html > head').append(style);
    }
    if(direction=="leftRight"){
      for(i=1;i<9;i*=2){
        $("#bincont").appendGridSpan(i);
      }
    }
    if(direction=="rightLeft"){
      for(i=8;i>=1;i-=(i/2)){
        $("#bincont").appendGridSpan(i);
      }
    }
    //Append dots, same for all directions
    appendBlank(8);
    appendDot(82);
    appendBlank(8);
    appendDot(84);
    appendBlank(8);
    appendDot(86);
    appendBlank(4);
    appendDot(42);
    appendDot(43);
    appendDot(44);
    appendDot(45);
    appendDot(46);
    appendDot(21);
    appendDot(22);
    appendDot(23);
    appendDot(24);
    appendDot(25);
    appendDot(26);
    appendDot(11);
    appendDot(12);
    appendDot(13);
    appendDot(14);
    appendDot(15);
    appendDot(16);
  };
  /************END DIRECTION PROTOTYPE***********/
   
   
  /*************BEGIN TICK PROTOTYPE*************/
  
  BinaryClock.prototype.tick=function(){
    $('div .dotfilled').clearDot();
    $('span .dotfilled').clearDot();
      var tdate=new Date();
      var h=tdate.getHours().toString();
      var m=tdate.getMinutes().toString();
      var s=tdate.getSeconds().toString();
    $("#digital").html(parseInt(h, 10).toString(2)+":"+parseInt(m, 10).toString(2)+":"+parseInt(s, 10).toString(2));
    
    if(h.length==1) h="0"+h;
    if(m.length==1) m="0"+m;
    if(s.length==1) s="0"+s;
    
    $("#actual").html(h+":"+m+":"+s);
    
    /******HOURS******/
    
    var hh1=h.charAt(0);
    var hh2=h.charAt(1);
    switch(hh1){
      case "0":
        break;
      case "1":
        $("#11").fillDot();
        break;
      case "2":
        $("#21").fillDot();
        break;
    }
    hh2=parseInt(hh2, 10);
    if(Math.log(hh2)/Math.log(2) % 1 === 0 || hh1==1){
       $("#"+parseInt(hh2, 10).toString()+2).removeClass('dot').addClass('dotfilled');
    }else if(hh2>8){
      $("#12").fillDot();
      $("#82").fillDot();
    }else if(hh2>4){
      $("#42").fillDot();
      if(hh2==5 || hh2==7) $("#12").fillDot();
      if(hh2>=6) $("#22").fillDot();
      if(hh2==7) $("#42").fillDot();
    }else{
      $("#12").fillDot();
      $("#22").fillDot();
    }//end if
    
    
    
    /*****MINUTES******/
    var mm1=m.charAt(0);
    var mm2=m.charAt(1);
    
    switch(mm1){
      case "0":
          break;
      case "1":
          $("#13").fillDot();
          break;
      case "3":
          $("#13").fillDot();
          /* falls through */
      case "2":
          $("#23").fillDot();
          break;
      case "5":
          $("#13").fillDot();
          /* falls through */
      case "4":
          $("#43").fillDot();
          break;
    }
    mm2=parseInt(mm2, 10);
    if(Math.log(mm2)/Math.log(2) % 1 === 0 || mm2==1){
       $("#"+mm2.toString()+4).fillDot();
    }else if(mm2>8){
      $("#14").fillDot();
      $("#84").fillDot();
    }else if(mm2>4){
      $("#44").fillDot();
      if(mm2==5 || mm2==7) $("#14").fillDot();
      if(mm2>=6) $("#24").fillDot();
      if(mm2==7) $("#44").fillDot();
    }else if(mm2==3){
      $("#14").fillDot();
      $("#24").fillDot();
    }//end if
    
    
    
    /*****SECONDS******/
    var ss1=s.charAt(0);
    var ss2=s.charAt(1);
    
    switch(ss1){
      case "0":
          break;
      case "1":
          $("#15").fillDot();
          break;
      case "3":
          $("#15").fillDot();
          /* falls through */
      case "2":
          $("#25").fillDot();
          break;
      case "5":
          $("#15").fillDot();
          /* falls through */
      case "4":
          $("#45").fillDot();
          break;
    }
    ss2=parseInt(ss2, 10);
    if(Math.log(ss2)/Math.log(2) % 1 === 0 || ss2==1){
       $("#"+ss2.toString()+6).fillDot();
    }else if(ss2>8){
      $("#16").fillDot();
      $("#86").fillDot();
    }else if(ss2>4){
      $("#46").fillDot();
      if(ss2==5 || ss2==7) $("#16").fillDot();
      if(ss2>=6) $("#26").fillDot();
      if(ss2==7) $("#46").fillDot();
    }else if(ss2==3){
      $("#16").fillDot();
      $("#26").fillDot();
    }//end if
    var a = setInterval(this.tick, 100);
  };
  
  /************END TICK PROTOTYPE************/
  
  //var clock = new BinaryClock(active dot, inactive dot)
  //Directions - topBottom, bottomTop, leftRight, rightLeft
  
  var clock = new BinaryClock("#EA6617", "#777");
  clock.direction("bottomTop");
  clock.tick();
});