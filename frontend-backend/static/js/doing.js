//全局变量

window.onload=function(){
	var obj={
		'progress':'progress'
	}
	$.ajax({
		url:'progress',
		type:'POST',
		data:JSON.stringify(obj),
		async:true,
		success:function(data){
			if (data='error') {
				//do nothing
			}
			else{
				$('h5.my-3').append(data['name'])
				$('div.progress-bar').css('width',data['valuenow']+'%')
				$('div.progress-bar span').text(data[valuenow]+'%')
			}
		}
	})
}

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
							+'视频通道'+String(Number($('#chanelchooseend').prev().attr('id').slice(-1))+1)
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
			if ($('#chanelchooseend').prev().attr('id').slice(-1)==0) {
				$('#chanelchooseend').prev().children('button.btn-outline-secondary').remove()
			}
			else{
				$('#chanelchooseend').prev().remove()
			}
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
				'deletefilename':findfirstchosed().text(),
				'nowfolder':''
			}
		}
		else{
			obj={
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
					console.log('error')
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
	console.log(folderlist)
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
	for (path in data) {
		if(data[path]=='dir'){
			$('#showboard').append($('<button>').attr('type','button').attr('class','btn btn-outline-info ml-3 border-0').attr('onclick','chosed(this)').append(
									$('<span>').attr('class','fa fa-square-o fa-lg mr-5 pr-5'),
									$('<br>'),
									$('<span>').attr('class','fa fa-folder fa-5x'),
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
			if(path.substr(-11)=='mvtojpg.jpg'){
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
}

function findfirstchosed(){
	return $('#showboard').children('button').children('span.fa-check-square-o').siblings('p')
}