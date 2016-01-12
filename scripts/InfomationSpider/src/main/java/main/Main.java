package main;

import java.util.List;

import dao.SchoolDAO;
import model.School;
import spider.Vinji_Spider_GetAllSchoolInformation;
import spider.Vinji_Spider_GetSunData;
import us.codecraft.webmagic.Spider;
import us.codecraft.webmagic.pipeline.ConsolePipeline;
import util.EXCELUtil;
import util.SchoolService;

public class Main {

	
	
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		
		
		
		//new Main().get211Information();
		
		//new Main().getSunInformation();
		
		//SchoolService.saveSchoolAndMajorToDataBase();
		//SchoolService.dealSchoolRank();
		SchoolService.dealSchoolSalary();
	}
	
	public void get211Information(){
		/*
		System.out.println("stage 0 start");
		Vinji_Spider stage1Spide = new Vinji_Spider(0);
		Spider.create(stage1Spide).addUrl(request).addPipeline(new ConsolePipeline()).thread(10).run();
		
		
		System.out.println("stage 1 start");
		Vinji_Spider stage2Spide = new Vinji_Spider(1);
		stage2Spide.requestList = stage1Spide.requestList;
		Spider.create(stage2Spide).addUrl(request).addPipeline(new ConsolePipeline()).thread(10).run();
		
		
		System.out.println("stage 2 start");
		Vinji_Spider stage3Spide = new Vinji_Spider(2);
		stage3Spide.requestList = stage2Spide.requestList;
		Spider.create(stage3Spide).addUrl(request).addPipeline(new ConsolePipeline()).thread(5).run();
		EXCELUtil.saveAsEXCEL(stage3Spide.schoolList);
		*/
		String request = "http://data.api.gkcx.eol.cn/soudaxue/queryProvinceScore.html?messtype=jsonp&url_sign=queryProvinceScore&provinceforschool=&schooltype=&page=1&size=10&keyWord=&schoolproperty=&schoolflag=&schoolsort=&province=&fsyear=&fstype=&zhaoshengpici=&suiji=&callback=";
		int index = 0;
		//i 438
		for(int i = 1; i< EXCELUtil.totalRows; i=EXCELUtil.currentRows){
			System.out.println("--------------------");
			System.out.println("iterator time : " + index);
			System.out.println("--------------------");
			List<School> schoolList = EXCELUtil.getOneSchoolAndMajor(i);
			System.out.println("stage 0 start");
			Vinji_Spider_GetAllSchoolInformation stage1Spide = new Vinji_Spider_GetAllSchoolInformation(0);
			stage1Spide.school = schoolList.get(0);
			Spider.create(stage1Spide).addUrl(request).addPipeline(new ConsolePipeline()).thread(10).run();
			
			
			System.out.println("stage 2 start");
			Vinji_Spider_GetAllSchoolInformation stage2Spide = new Vinji_Spider_GetAllSchoolInformation(2);
			stage2Spide.requestList = stage1Spide.requestList;
			stage2Spide.school = schoolList.get(0);
			Spider.create(stage2Spide).addUrl(request).addPipeline(new ConsolePipeline()).thread(10).run();
			
			System.out.println("stage 3 start");
			Vinji_Spider_GetAllSchoolInformation stage3Spide = new Vinji_Spider_GetAllSchoolInformation(3);
			stage3Spide.requestList = stage2Spide.requestList;
			stage3Spide.school = schoolList.get(0);
			Spider.create(stage3Spide).addUrl(request).addPipeline(new ConsolePipeline()).thread(10).run();
			
			
			EXCELUtil.saveAsEXCEL(stage3Spide.school,0,0);
			
		}
		System.out.println("success");
		
	}
	
	public void getSunInformation(){
		
		
			Spider.create(new Vinji_Spider_GetSunData())
	        .addUrl("http://gaokao.chsi.com.cn/zyk/pub/myd/specAppraisalTop.action?zgsx=211&start=0")
	        .addPipeline(new ConsolePipeline())
	        .thread(1).run();
			SchoolDAO.close();
			System.out.println("success");
	}

}
