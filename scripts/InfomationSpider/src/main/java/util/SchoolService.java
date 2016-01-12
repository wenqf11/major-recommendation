package util;

import java.util.List;

import dao.SchoolDAO;
import model.StoreageSchool;

public class SchoolService {

	public static void saveSchoolAndMajorToDataBase(){
		
		List<StoreageSchool> schools = EXCELUtil.getAllStoreSchoolAndMajor();
		
		SchoolDAO.saveComment(schools);
		
	}
	
	public static void dealSchoolRank(){
		
		List<StoreageSchool> schools = EXCELUtil.getSchoolRank();
		
		SchoolDAO.saveSchoolRank(schools);
		
	}
	
	public static void dealSchoolSalary(){
		
		
		List<StoreageSchool> schools = EXCELUtil.getMajorSalary();
		
		SchoolDAO.saveSalary(schools);
	}
}
