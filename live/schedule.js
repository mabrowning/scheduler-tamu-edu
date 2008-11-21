IE=(navigator.userAgent.toLowerCase().indexOf("msie")>-1)

//Global variables
//
//This contains the main calender body
var Calender=null;

//mouse flags
mouseUp=true;

//animation
animate=true;
speed=1;

ajax=new Ajax();
Courses=new Array();
Controllers=new Array();
var ControllerDIV=null;
var Hourspan=null;
hours=0;

//This function is called when there is an error in user input or in operation. Eventually, it will be implemented in an error bar, but for now, we alert();
function error(str){
	alert(str);
}

//This function is called body onload to initialize the calender to the included DIV
function Init()
{
	Calender = new CalenderBlock(document.getElementById('schedulecontainer'));
	courseget= new CourseGet();
	ControllerDIV=document.getElementById('controllerDIV');
	Hourspan=document.getElementById('hours');
}
//This class is the functional calender. It handles creating the DOM, sizing and distributing the TimeBlocks.
function CalenderBlock(content)
{
	this.content=content;
	this.start_hour=8;
	this.hours=12;
	this.percent_height=50/this.hours+"%";
	this.top_incr=50/this.hours;
	
	this.times=document.createElement('DIV'); 
	this.hourlabels=document.createElement('DIV'); 
	this.daysDIV=document.createElement('DIV');

	this.times.setAttribute('id','times');
	this.daysDIV.setAttribute('id','days');
	this.hourlabels.setAttribute('id','hourlabels');	

	for(i=this.start_hour;i<this.hours+this.start_hour;i++){
		hour=document.createElement('DIV');
		half=document.createElement('DIV');
		label=document.createElement('DIV');
		
		hour.className='hour';
		half.className='halfhour';
		label.className='hourlabel';
		
		hour.style.height=this.percent_height;
		half.style.height=this.percent_height;
		label.style.height=this.percent_height;
		
		hour.style.top=2*(i-this.start_hour   )*this.top_incr+"%";
		half.style.top=2*(i-this.start_hour+.5)*this.top_incr+"%";
		label.style.top= (i-this.start_hour+.5)*this.top_incr+"%";
	
		this.times.appendChild(hour);
		this.times.appendChild(half);
	
		label.innerHTML=(( i==0 || i==12 )?12:i%12)+":00 "+((i>11)?"PM":"AM");
		this.hourlabels.appendChild(label);
	}
	delete hour;
	delete half;
	delete label;
	this.content.appendChild(this.times);
	this.content.appendChild(this.hourlabels);
	this.days=[];
	day_ar=new Array("M","T","W","R","F");
	for(i=0;i<5;i++){
		day=document.createElement('DIV');
		day_bord=document.createElement('DIV');
		day.className='day';
		day_bord.className='daybord';
		day_bord.setAttribute('id',day_ar[i]);
		this.days[day_ar[i]]=day_bord;
		day.appendChild(day_bord)
		this.daysDIV.appendChild(day);
	}
	delete day_ar;
	this.content.appendChild(this.daysDIV);	
	this.Position = function(start)
	{
		return 100*(start.Hours()-this.start_hour)/this.hours+'%';
	} 
	this.Height = function(start,stop)
	{
		return 100*(stop.Hours()-start.Hours())/this.hours+'%';
	}
	this.colors=new Array("#FFE099","#F4FF99","#7CF7E2","#99C3FF","#7C90F7","#E47CF7","#FFB299");
	this.colorindex=0;
	this.GetNextColor = function()
	{
		return this.colors[this.colorindex++%this.colors.length];
	}
	this.highlighted=[];
	this.DeselectAll = function(){
		for(i in this.highlighted)
			this.highlighted[i].UnHighlight();
	}


}
//This class is representative of a time and parsing a string as a time.
function Time(str)
{
	this.hour=parseInt(str.substr(0,2),10);
	this.minute=parseInt(str.substr(3,5),10);
	this.hour+=(str[5]=='P'&&this.hour!=12?12:0);
	if(this.hour==12 && str[5]=='A')this.hour=0;

	this.GreaterThan = function(test)
	{
		if(this.hour<test.hour)return false;
		if(this.hour>test.hour || this.minute>test.minute)return true;
	}
	this.Hours = function()
	{
		return this.hour+this.minute/60;
	}
}
function SetOpacity(div,opacity){
	if(IE)
		div.style.filter='alpha(opacity='+opacity*100+')';
	else
		div.style.opacity=opacity;
}
function AnimateTimeBlock(tb,draw)
{
	if(draw){
		if(tb.drawing)return;
		if(tb.undrawing){
			window.clearInterval(tb.interval);
			tb.undrawing=false;
		}
		else{
			tb.opacity=0;
			SetOpacity(tb.oDIV,tb.opacity);
			Calender.days[tb.day].appendChild(tb.oDIV);
		}
		tb.drawing=true;
		tb.interval=window.setInterval(function(){
			tb.opacity=tb.opacity+.2;
			SetOpacity(tb.oDIV,tb.opacity);
			if(tb.opacity>.9){
				window.clearInterval(tb.interval);
				tb.drawing=false;
				tb.isdrawn=true;
			}
		},50/speed);

	}
	else{
		if(tb.undrawing)return;
		if(tb.drawing){
			window.clearInterval(tb.interval);
			tb.drawing=false;
		}
		tb.undrawing=true;
		tb.interval=window.setInterval(function(){
			tb.opacity=tb.opacity-.2;
			SetOpacity(tb.oDIV,tb.opacity);
			if(tb.opacity<0.1){
				window.clearInterval(tb.interval);
				tb.oDIV.parentNode.removeChild(tb.oDIV);
				tb.undrawing=false;
				tb.isdrawn=false;
			}
		},50/speed);
	}
}
//This class represents a single block of allocated time on the calender.
function TimeBlock(content,start_time,stop_time,day)
{
	this.id=content.substr(0,12);
	this.content=content.replace("\n","<BR/>\n");
	this.start_time=new Time(start_time);
	this.stop_time=new Time(stop_time);
	this.day=day;
	this.oDIV= document.createElement('DIV');
	this.oDIV.innerHTML=this.content;
	this.oDIV.setAttribute('title',start_time+" - "+stop_time);
	this.oDIV.className="timeblock";
	this.isdrawn=false;
	this.color="#FFFFFF";
	this.Draw = function(color,id)
	{
		if(color)this.color=color;
		this.oDIV.setAttribute('onclick',"Controllers["+id+"].Select();");
		this.oDIV.style.backgroundColor=this.color;
		this.oDIV.style.top=Calender.Position(this.start_time);
		this.oDIV.style.height=Calender.Height(this.start_time,this.stop_time);
		if(animate)AnimateTimeBlock(this,true);
		else{
			Calender.days[this.day].appendChild(this.oDIV);
			this.isdrawn=true;
		}
	}
	this.UnDraw = function()
	{
		this.oDIV.onclick=null;
		if(animate)AnimateTimeBlock(this);
		else{
			if(!this.isdrawn)return;
			if(this.oDIV.parentNode)this.oDIV.parentNode.removeChild(this.oDIV);
			this.isdrawn=false;
		}
	}
	this.Intersects = function(test)
	{
		if(!this.isdrawn || !test.isdrawn)return false;
		if(this.start_time.GreaterThan(test.start_time) &&
			test.stop_time.GreaterThan(this.start_time))return true;
		if(test.start_time.GreaterThan(this.start_time) &&
			this.stop_time.GreaterThan(test.start_time))return true;
		return false;
	}
	this.Highlight = function()
	{
		Calender.highlighted[this.id]=this;
		this.oDIV.className='timeblock highlighted';
	}
	this.UnHighlight = function()
	{
		delete Calender.highlighted[this.id];
		this.oDIV.className='timeblock';
	}
}
function Section(dept,course,section,TDR,prof,credit,descrip,seats,seatsa)
{
	this.dept=dept;
	this.course=course;
	this.section=section;
	this.TDR=TDR;
	this.prof=prof;
	this.credit=credit;
	this.descrip=descrip;
	this.seats=seats;
	this.seatsa=seatsa;
	this.timeblocks=[];
	str=dept+" "+course+" "+section+" - "+prof+"\n"
	for(var i in this.TDR)
		for(var j=0;j<5;j++)
			if(this.TDR[i][j]!=" ")
				this.timeblocks.push(new TimeBlock(str+this.TDR[i].substr(24),
					this.TDR[i].substring(8,15),
					this.TDR[i].substring(16,23),
					this.TDR[i][j]));
	delete str;
	this.Draw = function(color,id)
	{
		log('Section.Draw();');
		for(var i in this.timeblocks)
			this.timeblocks[i].Draw(color,id);
	}
	this.UnDraw = function()
	{
		log('Section.UnDraw();');
		for(var i in this.timeblocks)
			this.timeblocks[i].UnDraw();
	}
	this.Select = function()
	{
		for(var i in this.timeblocks)
			this.timeblocks[i].Highlight();
	}
	
}
function Course(course,str)
{
	temp=document.createElement('DIV');
	temp.innerHTML=str;
	temp=temp.firstChild;
	this.sections=Array();
	this.chosen=Array();
	this.course=course.substr(0,7);
	for(var i=0;i<temp.rows.length;i++)
	{//(dept,class,section,TDR,prof,credit,descrip,seats,seatsa)
		TDR=[];
		for(var j=6;j<11;j++)
			 if(temp.rows[i].cells[j].innerHTML!="")
				 TDR.push(temp.rows[i].cells[j].innerHTML)
		this.sections[temp.rows[i].cells[0].innerHTML]=new Section(
		course.substr(0,4),
		course.substr(4,3),
		temp.rows[i].cells[0].innerHTML,
		TDR,
		temp.rows[i].cells[1].innerHTML,
		temp.rows[i].cells[3].innerHTML,
		temp.rows[i].cells[2].innerHTML,
		temp.rows[i].cells[4].innerHTML,
		temp.rows[i].cells[5].innerHTML);
	}
	delete temp;
	this.Choose = function(section)
	{
		if(section==''||section==null)
		{
			log('Course.Choose: we were given a null section');
			for(sect in this.sections)
				if(!(sect in this.chosen))
				{
					section=sect;
					log('Course.Choose: we chose '+section);
					break;
				}
		}
		else if(!(section in this.sections))
			return null;
		delete sect;
		log('Course.Choose('+section+');');
		if(section in this.chosen){
			log("Course.Choose: we won't choose a duplicate section!");
/*			warn("Warning: You've already scheduled this section!");*/
			return false;
		}
		this.chosen[section]='';
		return this.sections[section];
	}
	this.UnChoose = function(section)
	{ 
		log('Course.UnChoose('+section+');');
		res=delete this.chosen[section];
		if(!res)log('Course.UnChoose: failed!');
		return res;
	}
}
function Controller(course,id)
{
	this.course=course;
	this.id=id;
	this.chosen='';
	this.color=Calender.GetNextColor();
	this.oDIV=document.createElement('DIV');
	this.oDIV.className='controller';
	this.oDIV.style.backgroundColor=this.color;
	//This was the old way of doing things
	str="<SELECT onchange='Controllers["+this.id+"].Choose(this.value);'>\n"
	for(sec in this.course.sections)
		str+="<OPTION VALUE='"+sec+"'>"+sec+" - "+this.course.sections[sec].descrip+"\n"
	str+="</SELECT>"
	str+="<a href=# onclick='Controllers["+this.id+"].Destroy();>X</a>";
	this.oDIV.innerHTML=str;
	delete str;
	ControllerDIV.appendChild(this.oDIV);
	this.Choose = function(section)
	{
		log('Controller.Choose('+section+');');
		try{
			this.course.UnChoose(this.chosen.section);
			this.chosen.UnDraw();
		}
		catch(e){
			log('Controller.Choose: handled error');
		}
		this.chosen=this.course.Choose(section);
		if(!this.chosen)return;
		log('Controller.Choose: we are drawing '+this.chosen.dept+this.chosen.course+this.chosen.section);
		this.chosen.Draw(this.color,this.id);

	}
	this.Select = function()
	{
		Calender.DeselectAll();
		this.chosen.Select();	
	}
	this.Destroy = function()
	{
		try{
			this.course.UnChoose(this.chosen.section);
			this.chosen.UnDraw();
		}
		catch(e){
			log("Controller.Destoy: handled error");
		}
		this.oDIV.parentNode.removeChild(this.oDIV);
		Controllers[this.id]=null;
	}
}
function Browser()
{
	return;
}

function entsub(event)
{
	if(event && event.keyCode == 13)
		courseget.GetCourse(curcor(),"");
}
function Ajax()
{
	this.error="Course doesn't exist..";
	this.callback=null;
	this.xmlhttp=null;
	if (window.XMLHttpRequest)
		this.xmlhttp=new XMLHttpRequest();
	else if (window.ActiveXObject)
		this.xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
	else
		error("No AJAX support in this browser... I'm half sad and half impressed...");
	this.Start = function(callback,URL,error)
	{
		this.xmlhttp.onreadystatechange=callback;
		this.error=(error==null)?"Generic Server Error:\nCould I be any more cyptic?":error;
/*		this.xmlready=false;*/
		this.xmlhttp.open('GET',URL,true);
		this.xmlhttp.send(null);
	}
	this.handle = function()
	{
		//handle should only be called from inside the current onreadystatechange callback function
		//returns true is callback should continue and false if it should stop
 		if(ajax.xmlhttp.readyState!=4 || ajax.xmlhttp.status!=200 || ajax.xmlhttp.responseText=='')return false;
		if(ajax.xmlhttp.responseText.indexOf('Query')>-1){
			error(ajax.error);
			ajax.xmlready=true;
			return false;
		}
		ajax.xmlready=true;
		return true;
	}

}
function curcor(){
	return document.getElementById('tdept').value.toUpperCase()+document.getElementById('tcourse').value;
}
function CourseGet() 
{
	this.course="";
	this.section="";
	this.GetCourse = function(course,section)
	{
		this.course=course;
		this.section=section;
		log("CourseGet.GetCourse("+this.course+");");
		if(this.course in Courses)
			this.AddController();
		else if(!ajax.xmlready)
			window.setTimeout(courseget.StartAjax,100);
		else{
			log("Starting StartAjax... "+this.course);
			this.StartAjax();
		}
	}
	this.AddController = function(){
		Controllers[Controllers.length] = new Controller(Courses[this.course],Controllers.length);
		Controllers[Controllers.length-1].Choose(this.section)
	}
	this.Callback = function(){
		if(!ajax.handle())return;
		Courses[courseget.course]=new Course(courseget.course,ajax.xmlhttp.responseText);
		courseget.AddController();
	}
	this.StartAjax = function(){
		log("CourseGet.StartAjax(); "+courseget.course);
		ajax.Start(courseget.Callback,'getclass.php?class='+courseget.course,"Course doesn't exist...");
	}
}

