package util;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import org.dom4j.Document;
import org.dom4j.DocumentException;
import org.dom4j.DocumentHelper;
import org.dom4j.Element;
import org.dom4j.io.SAXReader;
import org.dom4j.io.XMLWriter;

import model.School;

public class XMLUtil {
/*
	public static void saveAsXML(List<School> schoolList,int index) throws IOException
	{

		Document document = DocumentHelper.createDocument();
		Element xmlSchoolList = document.addElement("schoolList");
		for(School school : schoolList){
			
			Element xmlSchool = xmlSchoolList.addElement("school");
			Element xmlSchoolId = xmlSchool.addElement("schooleID");
			xmlSchoolId.addText(school.getSchooleID());
			Element xmlSchoolName = xmlSchool.addElement("schoolName");
			xmlSchoolName.addText(school.getSchoolName());
			Element xmlLocalProvince = xmlSchool.addElement("localProvince");
			xmlLocalProvince.addText(school.getLocalProvince());
			Element xmlStudentType = xmlSchool.addElement("studentType");
			xmlStudentType.addText(school.getStudentType());
			Element xmlYear = xmlSchool.addElement("year");
			xmlYear.addText(school.getYear());
			Element xmlBatch = xmlSchool.addElement(("batch"));
			xmlBatch.addText(school.getBatch());
			Element xmlVar = xmlSchool.addElement(("var"));
			xmlVar.addText(school.getVar());
			Element xmlVarScore = xmlSchool.addElement(("var_score"));
			xmlVarScore.addText(school.getVar_score());
			Element xmlMax = xmlSchool.addElement(("max"));
			xmlMax.addText(school.getMax());
			Element xmlMin = xmlSchool.addElement(("min"));
			xmlMin.addText(school.getMin());
			Element xmlNum = xmlSchool.addElement(("num"));
			xmlNum.addText(school.getNum());
			Element xmlFencha = xmlSchool.addElement(("fencha"));
			xmlFencha.addText(school.getFencha());
			Element xmlProvincescore = xmlSchool.addElement(("provincescore"));
			xmlProvincescore.addText(school.getProvincesScore());
			Element xmlURL = xmlSchool.addElement(("URL"));
			xmlURL.addText(school.getBatch());
		}
		
		XMLWriter output = new XMLWriter(new FileWriter(new File("schoolList"+index+".xml")));
		
		output.write(document);
		output.close();
		
		
		
	}
	*/
	public static List<School> getListFromFile(String fileName){
		
		List<School> schoolList = new ArrayList<School>();
		
		SAXReader reader = new SAXReader();
		File file = new File(fileName);
		
		Document document;
		try {
			
			document = reader.read(file);
			Element root = document.getRootElement();
			List<Element> xmlSchoolList = root.elements();
			
			for(Element xmlSchool : xmlSchoolList){
				List<Element> xmlTags = xmlSchool.elements();
				School school = new School();
				school.setSchooleID(xmlTags.get(0).getText());
				school.setSchoolName(xmlTags.get(1).getText());
			//	school.setLocalProvince(xmlTags.get(2).getText());
				//school.setStudentType(xmlTags.get(3).getText());
				schoolList.add(school);
			}
			
		} catch (DocumentException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		
		return schoolList;
	} 
	
}
