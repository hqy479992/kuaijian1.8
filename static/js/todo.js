'use strict'
//全局变量

//todo界面show函数需要简化！！！！！！！！！bootstrap4风格tooltip需要添加

//是否正在选择通道，默认否，在隐藏面板出现事件触发时变为是，隐藏面板隐藏事件触发变为否
var chooseingchanel=false
//所选文件夹中是否含有音频文件夹
var hasAudio=false
//音频文件夹名字记录下来
var audioFolder=''
//已选中的通道文件夹数组
var folderlist=new Array()

window.onload=function(){
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

//click事件
//新增的button以及button组添加一个类newadded，便于合成识别
var chosed=function(buttonobj){
	if(buttonobj.innerHTML.lastIndexOf('fa-square-o')!=-1){
		$(buttonobj).html(buttonobj.innerHTML.replace('fa-square-o','fa-check-square-o'))
		if(chooseingchanel==true){
			if ($('#chanelchooseend').prev().attr('id').slice(-1)==0 && $('#chanelchooseend').prev().children('button.btn-outline-secondary').length==0) {
				$('#chanelchooseend').prev().append($('<button>').attr('type','button').attr('class','btn btn-outline-secondary newadded').attr('disabled','true').append(
														$(buttonobj).attr('data-original-title')))
			}
			else{
				var newchanel='<div class="btn-group ml-3 btn-group-sm pb-1 mb-1 newadded" role="group" id="chanel'
							+String(Number($('#chanelchooseend').prev().attr('id').slice(-1))+1)
							+'"><button type="button" class="btn btn-secondary" disabled="true">'
							+'通道'+$('#collapsechanelchoose').children().children('div').length.toString()
							+'</button></div>'
				$('#chanelchooseend').before(newchanel)
				$('#chanelchooseend').prev().append($('<button>').attr('type','button').attr('class','btn btn-outline-secondary').attr('disabled','true').append(
														$(buttonobj).attr('data-original-title')))
			}
			if ($(buttonobj).html().indexOf('fa-music')!=-1) {
				hasAudio=true
				audioFolder=$(buttonobj).attr('data-original-title')
			}
		}
	}
	else{
		$(buttonobj).html(buttonobj.innerHTML.replace('fa-check-square-o','fa-square-o'))
		if (chooseingchanel==true) {
			/*<button type="button" class="btn btn-outline-secondary" disabled="disabled">新建文件夹</button>*/
			$('#collapsechanelchoose').find('button.btn-outline-secondary').each(function(){
				if($(this).text()==$(buttonobj).attr('data-original-title')){
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
		//没有被选择的文件
	}
	else{
		//知道执行该操作时所在的具体文件夹路径是为了及时更新操作后的结果，给用户即时感
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
				}
				else{
					showdirs(data)
				}
			}
		})
	}
	$('#deletefilemodal').modal('hide')
})

$('#surerename').click(function(){
	if (findfirstchosed().text()=='') {
		//do nothing
	}
	else{
		var folderin=findfirstchosed().parent().attr('data-original-title').lastIndexOf('/')
		var newname=document.getElementById('newName').value
		if (newname=='') {
			//do nothing
			$('#nameError').html('ERROR!必填！<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>')
			$('#nameError').attr('class','alert alert-danger alert-dismissible fade mt-2 show')
		}
		else{
			var obj
			if (folderin==-1) {
				obj={
					'originname':findfirstchosed().parent().attr('data-original-title'),
					'nowfolder':'',
					'newname':newname
				}
			}
			else{
				obj={
					'originname':findfirstchosed().parent().attr('title'),
					'nowfolder':findfirstchosed().parent().attr('title').slice(0,folderin)+'/',
					'newname':newname
				}
			}
			$.ajax({
				url:'renamefile',
				type:'POST',
				data:JSON.stringify(obj),
				async:true,
				success:function(data){
					if (data=='error') {
						$('#nameError').html('ERROR!非法字符！<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>')
					}
					else{
						$('#renamemodal').modal('hide')
						showdirs(data)
					}
				}
			})
		}
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
	folderlist=new Array()
	//先获取已经选择的文件夹
	for (var i = 0; i < $('#collapsechanelchoose').find('.newadded').length; i++) {
		if (i==0) {
			folderlist[i]=$('#collapsechanelchoose').find('.newadded').eq(0).text()
		}
		else{
			folderlist[i]=$('#collapsechanelchoose').find('.newadded').eq(i).children('button.btn-outline-secondary').text()
		}
	}
	//检测有无音频文件夹
	//传给后端的是folderlist(包含音频)以及audiofolder
	if(!hasAudio){
		//没有音频文件夹的情况下，选一个视频文件夹作为音频通道
		$('#chooseaudiomodal').find('.list-group').html('')
		for (var i = 0; i < folderlist.length; i++) {
			$('#chooseaudiomodal').find('.list-group').append(
				$('<button>').attr('type','button').attr('class','list-group-item list-group-item-action').attr('onclick','chooseaudio(this)').append(
					folderlist[i]))
		}
		$('#chooseaudiomodal').modal('show')
	}
	if (hasAudio&&audioFolder!='') {
		var obj={
			'videoAudiolist':folderlist,
			'audioFolder':audioFolder,
			'audioByVideo':false
		}
		console.log(JSON.stringify(obj))
		$.ajax({
			url:'/synfolderlist',
			type:'POST',
			data:JSON.stringify(obj),
			async:true,
			success:function(data){
				if(data=='success'){
					window.location.href='/settings?chanelsum='+(folderlist.length-1).toString()
				}
				else{
					// do nothing
				}
			}
		})
	}
})

function chooseaudio(thisbutton){
	hasAudio=true
	audioFolder=$(thisbutton).text()
	$(thisbutton).attr('class','list-group-item list-group-item-action active')
	$(thisbutton).siblings('button').attr('class','list-group-item list-group-item-action')
}

$('#startsynvideolist').click(function(){
	if (hasAudio&&audioFolder!='') {
		console.log(JSON.stringify(obj))
		var obj={
			'videoAudiolist':folderlist,
			'audioFolder':audioFolder,
			'audioByVideo':true
		}
		$.ajax({
			url:'/synfolderlist',
			type:'POST',
			data:JSON.stringify(obj),
			async:true,
			success:function(data){
				if (data=='success') {
					window.location.href='/settings?chanelsum='+folderlist.length
				}
				else{
					//donothing
				}
			}
		})
	}
})

//show事件
$('#deletefilemodal').on('show.bs.modal',function(event){
	if(findfirstchosed().text()==''){
		$('#deletefilename').html('未选择文件！')
	}
	else{
		$('#deletefilename').html('将要删除 '+findfirstchosed().text()+' ！删除后将不可恢复！')
	}
})

$('#renamemodal').on('show.bs.modal',function(event){
	if (findfirstchosed().text()=='') {
		$('#originName').attr('value','未选择文件！')
	}
	else{
		$('#originName').attr('value',findfirstchosed().parent().attr('title'))
	}
})

$('#collapsechanelchoose').on('show.bs.collapse',function(event){
	chooseingchanel=true
	//每次重新选择，hasAudio都要变为false
	hasAudio=false
	audioFolder=''
	//所有原来已经点击选中的文件取消选中
	$('#showboard').find('span.fa-check-square-o').attr('class','fa fa-square-o fa-lg mr-5 pr-5')
	//保证每次点击合成按钮后都是新的可供选择的通道
	$('#collapsechanelchoose').find('.newadded').remove()
})

$('#collapsechanelchoose').on('hide.bs.collapse',function(argument) {
	chooseingchanel=false
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
		var basicbuttonbegin='<button type="button" class="btn btn-outline-info ml-3 border-0" onclick="chosed(this)" data-toggle="tooltip" data-original-title="'
						+path
						+'" title="'
						+path
						+'"><span class="fa fa-square-o fa-lg mr-5 pr-5"></span><br>'
		var basicbuttonend='<br><p>'
							+path.substr(0,20)
							+'</p></button>'
		if(data[path]=='dir'){
			$('#showboard').append(basicbuttonbegin
									+'<span class="fa fa-folder fa-5x"></span>'
									+basicbuttonend)
		}
		else if (data[path]=='musicdir') {
			$('#showboard').append(basicbuttonbegin
									+'<span class="fa-stack fa-2x my-2"><i class="fa fa-folder-o fa-stack-2x"></i><i class="fa fa-music fa-stack-1x"></i></span>'
									+basicbuttonend)
		}
		else if(only_audio_suffix.includes(data[path].toLowerCase())){
			$('#showboard').append(basicbuttonbegin
									+'<span class="fa-stack fa-2x my-2"><i class="fa fa-file-o fa-stack-2x"></i><i class="fa fa-music fa-stack-1x"></i></span>'
									+basicbuttonend)
		}
		else if(video_suffix.includes(data[path].toLowerCase())){
			$('#showboard').append(basicbuttonbegin
									+'<img src="static/uploadfiles/'+path.slice(0,-4)+'mvtojpg.jpg" class="showmvimg">'
									+basicbuttonend)
		}
		else if(data[path]=='.xml'){
			$('#showboard').append(basicbuttonbegin
									+'<span class="fa fa-file-code-o fa-4x my-2"></span>'
									+basicbuttonend)
		}
		else if (img_suffix.includes(data[path].toLowerCase())) {
			if(path.substr(0-'mvtojpg.jpg'.length)=='mvtojpg.jpg'){
				//do nothing
			}
			else{
				$('#showboard').append(basicbuttonbegin
										+'<img src="static/uploadfiles/'+path+'" class="showmvimg">'
										+basicbuttonend)
			}
		}
		else{
			$('#showboard').append(basicbuttonbegin
									+'<span class="fa fa-file-o fa-4x my-2"></span>'
									+basicbuttonend)
		}
	}
	$('[data-toggle="tooltip"]').tooltip()
	if (chooseingchanel==true) {
		if($('#collapsechanelchoose').find('button.btn-outline-secondary').length==0){
			//do nothing
		}
		else{
			$('#collapsechanelchoose').find('button.btn-outline-secondary').each(function(){
				var chosedname=$(this).text()
				$('#showboard').find('p').each(function(){
					if ($(this).text()==chosedname) {
						$(this).parent().find('span').first().attr('class','fa fa-check-square-o fa-lg mr-5 pr-5')
					}
				})
			})
		}
	}
}

function findfirstchosed(){
	return $('#showboard').children('button').children('span.fa-check-square-o').first().siblings('p')
}

//oninput事件，随时监听input的输入值，一旦输入就会执行下面的函数
var nameInfo=function(){
	$('#nameError').attr('class','alert alert-danger alert-dismissible fade mt-2')
	$('#nameError').html('')
}