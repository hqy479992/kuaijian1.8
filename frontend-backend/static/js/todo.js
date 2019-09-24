'use strict'
//全局变量
var chooseingchanel=false

window.onload=function(){
	$('#header').load('header')
	$('nav.col-2').load('navbar')
	var obj={
		'type':'upload'
	}
	$.ajax({
		url:'getdirsbyupload',
		type:'POST',
		data:JSON.stringify(obj),
		async:true,
		success:function(data){
			if(data=='error'){
				//donongthing
			}
			else{
				showdirs(data)
			}
		}
	})
}

//现在感觉一周前写的代码是坨不可修复的烂泥
//click事件
var chosed=function(buttonobj){
	if(buttonobj.innerHTML.lastIndexOf('fa-square-o')!=-1){
		$(buttonobj).html(buttonobj.innerHTML.replace('fa-square-o','fa-check-square-o'))
		if(chooseingchanel==true){
			if ($('#chanelchooseend').prev().attr('id').slice(-1)==0 && $('#chanelchooseend').prev().children('button.btn-outline-secondary').length==0) {
				$('#chanelchooseend').prev().append($('<button>').attr('type','button').attr('class','btn btn-outline-secondary').attr('disabled','true').append(
														$(buttonobj).children('p').html()))
			}
			else{
				var newchanel='<div class="btn-group ml-3 btn-group-sm pb-1 mb-1" role="group" id="chanel'
							+String(Number($('#chanelchooseend').prev().attr('id').slice(-1))+1)
							+'"><button type="button" class="btn btn-secondary" disabled="true">'
							+'通道'+String(Number($('#chanelchooseend').prev().attr('id').slice(-1))+2)
							+'</button></div>'
				$('#chanelchooseend').before(newchanel)
				$('#chanelchooseend').prev().append($('<button>').attr('type','button').attr('class','btn btn-outline-secondary').attr('disabled','true').append(
														$(buttonobj).children('p').html()))
			}
		}
	}
	else{
		$(buttonobj).html(buttonobj.innerHTML.replace('fa-check-square-o','fa-square-o'))
		if (chooseingchanel==true) {
			/*<button type="button" class="btn btn-outline-secondary" disabled="disabled">新建文件夹</button>*/
			$('#collapsechanelchoose').find('button.btn-outline-secondary').each(function(){
				if($(this).text()==$(buttonobj).children('p').text()){
					$(this).parent().remove()
					if ($('#collapsechanelchoose').find('button.btn-secondary').length==0) {
						$('#chanelchooseend').before('<div class="btn-group ml-3 btn-group-sm mb-1 pb-1" role="group" aria-label="First group" id="chanel0">'+
														'<button type="button" class="btn btn-secondary" disabled="true">通道1</button>'+
													'</div>')
					}
					var i=1
					$('#collapsechanelchoose').find('button.btn-secondary').each(function(){
						$(this).text('通道'+i)
						i++
					})
				}
			})
		}
	}
}

$('#suredelete').click(function(){
	if(findfirstchosed().text()==''){
		//do nothing
	}
	else{
		var folderin=findfirstchosed().text().lastIndexOf('/')
		var obj
		if (folderin==-1) {
			obj={
				'path':'static/uploadfiles',
				'deletefilename':findfirstchosed().text(),
				'nowfolder':''
			}
		}
		else{
			obj={
				'path':'static/uploadfiles',
				'deletefilename':findfirstchosed().text(),
				'nowfolder':findfirstchosed().text().slice(0,folderin)+'/'
			}
		}
		$.ajax({
			url:'deletefile',
			type:'POST',
			data:JSON.stringify(obj),
			async:true,
			success:function(data){
				if(data=='error'){
					//do nothing
				}
				else{
					$('#deletefilemodal').modal('hide')
					showdirs(data)
				}
			}
		})
	}
})

$('#openfolder').click(function(){
	if (findfirstchosed().text()=='') {
		//do nothing
	}
	else{
		var obj={
			'openfolder':findfirstchosed().text()+'/'
		}
		$.ajax({
			url:'/openfolder',
			type:'POST',
			data:JSON.stringify(obj),
			async:true,
			success:function(data){
				if (data=='error') {
					//do nothing
				}
				else{
					showdirs(data)
				}
			}
		})
	}
})

$('#backtoprevious').click(function(){
	if ($('#showboard button:first').children('p').text().indexOf('/')==-1) {
		//do nothing
	}
	else{
		var foldernameend=$('#showboard button:first').children('p').text().lastIndexOf('/')
		var obj
		if(foldernameend==$('#showboard button:first').children('p').text().indexOf('/')){
			obj={
				'backtoprevious':''
			}
		}
		else{
			var parentfolder=$('#showboard button:first').children('p').text().slice(0,foldernameend)
			obj={
				'backtoprevious':parentfolder.slice(0,parentfolder.lastIndexOf('/'))+'/'
			}
		}
		$.ajax({
			url:'/backtoprevious',
			type:'POST',
			data:JSON.stringify(obj),
			async:true,
			success:function(data){
				if(data=='error'){
					//donothing
				}
				else{
					showdirs(data)
				}
			}
		})
	}
})

$('#startsettings').click(function(){
	var folderlist=new Array()
	var folderlistend=$('#chanelchooseend').prev().attr('id').slice(-1)
	for (var i = 0; i <= Number(folderlistend); i++) {
		folderlist[i]=$('#chanel'+i.toString()).children('button.btn-outline-secondary').text()
	}
	if (folderlist.length<=1) {
		//do nothing
	}
	else{
		$.ajax({
			url:'/synfolderlist',
			type:'POST',
			data:JSON.stringify(folderlist),
			async:true,
			success:function(data){
				if(data=='success'){
					window.location.href='/settings?chanelsum='+folderlist.length.toString()
				}
				else{
					// do nothing
				}
			}
		})
	}
})

//show事件
$('#deletefilemodal').on('show.bs.modal',function(event){
	if(findfirstchosed().text()==''){
		$('#deletefilename').append('未选择文件！')
	}
	else{
		$('#deletefilename').append('将要删除 '+findfirstchosed().text()+' ！删除后将不可恢复！')
	}
})

$('#collapsechanelchoose').on('show.bs.collapse',function(event){
	chooseingchanel=true
})

//其他函数
function getParams(key){
	var reg=new RegExp('(^|&)'+key+'=([^&]*)(&|$)')
	var r=window.location.search.substr(1).match(reg)
	if(r!=null){
		return decodeURI(r[2])
	}
	return null
}

function showdirs(data){
	$('#showboard').html('')
	data=JSON.parse(data)
	for (var path in data) {
		if(data[path]=='dir'){
			$('#showboard').append($('<button>').attr('type','button').attr('class','btn btn-outline-info ml-3 border-0').attr('onclick','chosed(this)').append(
									$('<span>').attr('class','fa fa-square-o fa-lg mr-5 pr-5'),
									$('<br>'),
									$('<span>').attr('class','fa fa-folder fa-5x'),
									$('<br>'),
									$('<p>').append(path)))
		}
		else if (data[path]=='musicdir') {
			$('#showboard').append($('<button>').attr('type','button').attr('class','btn btn-outline-info ml-3 border-0').attr('onclick','chosed(this)').append(
									$('<span>').attr('class','fa fa-square-o fa-lg mr-5 pr-5'),
									$('<br>'),
									$('<span>').attr('class','fa-stack fa-2x my-2').append(
										$('<i>').attr('class','fa fa-folder-o fa-stack-2x'),
										$('<i>').attr('class','fa fa-music fa-stack-1x')),
									$('<br>'),
									$('<p>').append(path)))
		}
		else if(data[path]=='.mp3'){
			$('#showboard').append($('<button>').attr('type','button').attr('class','btn btn-outline-info ml-3 border-0').attr('onclick','chosed(this)').append(
									$('<span>').attr('class','fa fa-square-o fa-lg mr-5 pr-5'),
									$('<br>'),
									$('<span>').attr('class','fa-stack fa-2x my-2').append(
										$('<i>').attr('class','fa fa-file-o fa-stack-2x'),
										$('<i>').attr('class','fa fa-music fa-stack-1x')),
									$('<br>'),
									$('<p>').append(path)))
		}
		else if(data[path]=='.mp4'){
			$('#showboard').append($('<button>').attr('type','button').attr('class','btn btn-outline-info ml-3 border-0').attr('onclick','chosed(this)').append(
									$('<span>').attr('class','fa fa-square-o fa-lg mr-5 pr-5'),
									$('<br>'),
									$('<img>').attr('src','static/uploadfiles/'+path.slice(0,-4)+'mvtojpg.jpg').attr('class','showmvimg'),
									$('<p>').append(path)))
		}
		else if(data[path]=='.xml'){
			$('#showboard').append($('<button>').attr('type','button').attr('class','btn btn-outline-info ml-3 border-0').attr('onclick','chosed(this)').append(
									$('<span>').attr('class','fa fa-square-o fa-lg mr-5 pr-5'),
									$('<br>'),
									$('<span>').attr('class','fa fa-file-code-o fa-4x my-2'),
									$('<br>'),
									$('<p>').append(path)))
		}
		else if (data[path]=='.jpg') {
			if(path.substr(0-'mvtojpg.jpg'.length)=='mvtojpg.jpg'){
				//do nothing
			}
			else{
				$('#showboard').append($('<button>').attr('type','button').attr('class','btn btn-outline-info ml-3 border-0').attr('onclick','chosed(this)').append(
										$('<span>').attr('class','fa fa-square-o fa-lg mr-5 pr-5'),
										$('<br>'),
										$('<img>').attr('src','static/uploadfiles/'+path+'.jpg').attr('class','showmvimg'),
										$('<p>').append(path)))
			}
		}
		else{
			$('#showboard').append($('<button>').attr('type','button').attr('class','btn btn-outline-info ml-3 border-0').attr('onclick','chosed(this)').append(
									$('<span>').attr('class','fa fa-square-o fa-lg mr-5 pr-5'),
									$('<br>'),
									$('<span>').attr('class','fa fa-file-o fa-4x my-2'),
									$('<br>'),
									$('<p>').append(path)))
		}
	}
	if (chooseingchanel==true) {
		if($('#collapsechanelchoose').find('button.btn-outline-secondary').length==0){
			//do nothing
		}
		else{
			$('#collapsechanelchoose').find('button.btn-outline-secondary').each(function(){
				var chosedname=$(this).text()
				$('#showboard').find('p').each(function(){
					if ($(this).text()==chosedname) {
						console.log($(this).parent().find('span').last().attr('class'))
						$(this).parent().children('span.fa-square-o').html().replace('fa-square-o','fa-check-square-o')
					}
				})
			})
		}
	}
}

function findfirstchosed(){
	return $('#showboard').children('button').children('span.fa-check-square-o').siblings('p')
}