package util;

import java.util.ArrayList;
import java.util.List;

import junit.framework.TestCase;
import model.Major;
import model.School;

public class EXCELUtilTest extends TestCase {

	/*
	public void testWrite(){
		
		List<School> list = new ArrayList<School>();
		School school = new School();
		school.setSchoolName("清华大学");
		
		Major major = new Major();
		major.setSpecialtyname("软件");
		
		Major major1 = new Major();
		major1.setSpecialtyname("软件");
		Major major2 = new Major();
		major2.setSpecialtyname("软件");
		Major major3 = new Major();
		major3.setSpecialtyname("软件");
		Major major4 = new Major();
		major4.setSpecialtyname("软件");
		Major major5 = new Major();
		major5.setSpecialtyname("软件");
		
		school.getMajorList().add(major);
		school.getMajorList().add(major1);
		school.getMajorList().add(major2);
		school.getMajorList().add(major3);
		school.getMajorList().add(major4);
		school.getMajorList().add(major5);
		list.add(school);
		EXCELUtil.saveAsEXCEL(list);
	}
	*/
	public void testGetAllSchoolAndMajor(){
		
		List<School> schoolList = EXCELUtil.getAllSchoolAndMajor();
		
		this.assertNotNull(schoolList);
	}
}
