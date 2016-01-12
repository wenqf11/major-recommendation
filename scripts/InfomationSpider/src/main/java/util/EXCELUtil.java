package util;

import java.io.File;
import java.io.FileInputStream;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.List;

import jxl.Cell;
import jxl.Sheet;
import jxl.Workbook;
import jxl.write.Label;
import jxl.write.WritableSheet;
import jxl.write.WritableWorkbook;
import model.Major;
import model.School;
import model.StoreageMajor;
import model.StoreageSchool;   
  
    
  
public class EXCELUtil
  
{ 
	public static int currentRows = 1;
	public static int totalRows = Integer.MAX_VALUE;
	public static List<String> getAllProvince(){
		

		List<String> provinceList = new ArrayList<String>();
		
		jxl.Workbook readwb = null;   
		  
        try    
  
        {   
  
            //构建Workbook对象, 只读Workbook对象   
  
            //直接从本地文件创建Workbook   
  
            InputStream instream = new FileInputStream("省会.xls");   
  
            readwb = Workbook.getWorkbook(instream);   
  
    
  
            //Sheet的下标是从0开始   
  
            //获取第一张Sheet表   
  
            Sheet readsheet = readwb.getSheet(0);   
  
            //获取Sheet表中所包含的总列数   
  
            int rsColumns = readsheet.getColumns();   
  
            //获取Sheet表中所包含的总行数   
  
            int rsRows = readsheet.getRows();   
            
            //获取指定单元格的对象引用   

            for (int i = 1; i < rsRows; i++)   
            {   
     
  
                    Cell cell = readsheet.getCell(0, i);   
                    String provinceName = cell.getContents();
                    provinceList.add(provinceName);
  
            }   
        } catch (Exception e) {   
        	  
            e.printStackTrace();   
  
        } finally {   
  
            readwb.close();   
  
        }  
		
		return provinceList;
	}
	
	public static List<School> getOneSchoolAndMajor(int rows){


		List<School> schoolList = new ArrayList<School>();
		
		jxl.Workbook readwb = null;   
		
		List<String> provinceList = getAllProvince();
        try    
  
        {   
  
            //构建Workbook对象, 只读Workbook对象   
  
            //直接从本地文件创建Workbook   
  
            InputStream instream = new FileInputStream("211学校以及专业");   
  
            readwb = Workbook.getWorkbook(instream);   
  
    
  
            //Sheet的下标是从0开始   
  
            //获取第一张Sheet表   
  
            Sheet readsheet = readwb.getSheet(0);   
  
            //获取Sheet表中所包含的总列数   
  
  
            //获取Sheet表中所包含的总行数   
  
            int rsRows = readsheet.getRows();   
  
            //获取指定单元格的对象引用   
  
            String  preSchoolName =  readsheet.getCell(1, rows - 1).getContents();
            School preSchool = new School();
            preSchool.setSchoolName(preSchoolName);
            totalRows = rsRows;
            currentRows = rows;
            for (int i = rows; i < rsRows; i++)   
            {   
     
  
                    Cell cell = readsheet.getCell(1, i);   
                    String schoolName = cell.getContents();
                    cell = readsheet.getCell(2, i);
                    String majorName = cell.getContents();
                    currentRows ++;
                    if(!preSchool.getSchoolName().equals(schoolName)){
                    	
                    	schoolList.add(preSchool);
                    	
                    	break;
                    	
                    }
                    for(int year = 2006; year < 2015; year ++){
                    	for(String provinceName :provinceList){
		                    Major major = new Major();
		                	major.setSpecialtyname(majorName);
		                	major.setYear(year + "");
		                	major.setLocalProvince(provinceName);
		                	major.setVar("0");
		                	major.setVar_score("0");
		                	major.setStudentType("文科");
		                	
		                	Major major1 = new Major();
		                	major1.setSpecialtyname(majorName);
		                	major1.setYear(year + "");
		                	major1.setLocalProvince(provinceName);
		                	major1.setVar("0");
		                	major1.setVar_score("0");
		                	major1.setStudentType("理科");
		                	
		                    preSchool.getMajorList().add(major);
		                    preSchool.getMajorList().add(major1);
                    	}
                    }
  
            }
            schoolList.add(preSchool);
        } catch (Exception e) {   
        	  
            e.printStackTrace();   
  
        } finally {   
  
            readwb.close();   
  
        }  
		
		return schoolList;
	}
	

	public static List<StoreageSchool> getMajorSalary(){



		List<StoreageSchool> schoolList = new ArrayList<StoreageSchool>();
		
		jxl.Workbook readwb = null;   
	
        try    
  
        {   
  
            //构建Workbook对象, 只读Workbook对象   
  
            //直接从本地文件创建Workbook   
  
            InputStream instream = new FileInputStream("salary.xls");   
  
            readwb = Workbook.getWorkbook(instream);   
  
    
  
            //Sheet的下标是从0开始   
  
            //获取第一张Sheet表   
  
            Sheet readsheet = readwb.getSheet(0);   
  
            //获取Sheet表中所包含的总列数   
  
            int rsColumns = readsheet.getColumns();   
  
            //获取Sheet表中所包含的总行数   
  
            int rsRows = readsheet.getRows();   
  
            //获取指定单元格的对象引用   
  
            String  preSchoolName =  readsheet.getCell(0, 0).getContents();
            StoreageSchool preSchool = new StoreageSchool();
            preSchool.setSchoolName(preSchoolName);
            
            for (int i = 1; i < rsRows; i++)   
            {   
     
  
                    Cell cell = readsheet.getCell(0, i);   
                    String schoolName = cell.getContents();
                    cell = readsheet.getCell(1, i);
                    String majorName = cell.getContents();
                    cell = readsheet.getCell(2,i);
                    String salary = cell.getContents();
                    salary = salary.substring(0, salary.indexOf("元"));
                    
                    if(!preSchool.getSchoolName().equals(schoolName)){
                    	
                    	schoolList.add(preSchool);
                    	preSchool = new StoreageSchool();
                    	preSchool.setSchoolName(schoolName);
                    	
                    }
                    
                    	
                    StoreageMajor major = new StoreageMajor();
                	major.setMajorName(majorName);
                	major.setSalary(Double.parseDouble(salary));
                    preSchool.getMajors().add(major);
		                    
                    
            }
            schoolList.add(preSchool);
        } catch (Exception e) {   
        	  
            e.printStackTrace();   
  
        } finally {   
  
            readwb.close();   
  
        }  
		
		return schoolList;
	}
	

	public static List<StoreageSchool> getSchoolRank(){


		List<StoreageSchool> schoolList = new ArrayList<StoreageSchool>();
		
		jxl.Workbook readwb = null;   
	
        try    
  
        {   
  
            //构建Workbook对象, 只读Workbook对象   
  
            //直接从本地文件创建Workbook   
  
            InputStream instream = new FileInputStream("中国大学排名.xls");   
  
            readwb = Workbook.getWorkbook(instream);   
  
    
  
            //Sheet的下标是从0开始   
  
            //获取第一张Sheet表   
  
            Sheet readsheet = readwb.getSheet(0);   
  
            //获取Sheet表中所包含的总列数   
  
            int rsColumns = readsheet.getColumns();   
  
            //获取Sheet表中所包含的总行数   
  
            int rsRows = readsheet.getRows();   
  
            //获取指定单元格的对象引用   
  
            for (int i = 1; i < rsRows; i++)   
            {   
     
  
                    Cell cell = readsheet.getCell(0, i);   
                    String schoolName = cell.getContents();
                    cell = readsheet.getCell(1, i);
                    String score = cell.getContents();
                    StoreageSchool school = new StoreageSchool();
                    school.setSchoolName(schoolName);
                    school.setScore(Double.parseDouble(score));
                    schoolList.add(school);
            }
            
        } catch (Exception e) {   
        	  
            e.printStackTrace();   
  
        } finally {   
  
            readwb.close();   
  
        }  
		
		return schoolList;
	}
	

	public static List<StoreageSchool> getAllStoreSchoolAndMajor(){


		List<StoreageSchool> schoolList = new ArrayList<StoreageSchool>();
		
		jxl.Workbook readwb = null;   
	
        try    
  
        {   
  
            //构建Workbook对象, 只读Workbook对象   
  
            //直接从本地文件创建Workbook   
  
            InputStream instream = new FileInputStream("211学校以及专业");   
  
            readwb = Workbook.getWorkbook(instream);   
  
    
  
            //Sheet的下标是从0开始   
  
            //获取第一张Sheet表   
  
            Sheet readsheet = readwb.getSheet(0);   
  
            //获取Sheet表中所包含的总列数   
  
            int rsColumns = readsheet.getColumns();   
  
            //获取Sheet表中所包含的总行数   
  
            int rsRows = readsheet.getRows();   
  
            //获取指定单元格的对象引用   
  
            String  preSchoolName =  readsheet.getCell(1, 1).getContents();
            StoreageSchool preSchool = new StoreageSchool();
            preSchool.setSchoolName(preSchoolName);
            
            for (int i = 1; i < rsRows; i++)   
            {   
     
  
                    Cell cell = readsheet.getCell(1, i);   
                    String schoolName = cell.getContents();
                    cell = readsheet.getCell(2, i);
                    String majorName = cell.getContents();
                    
                    if(!preSchool.getSchoolName().equals(schoolName)){
                    	
                    	schoolList.add(preSchool);
                    	preSchool = new StoreageSchool();
                    	preSchool.setSchoolName(schoolName);
                    	
                    }
                    
                    	
                    StoreageMajor major = new StoreageMajor();
                	major.setMajorName(majorName);
                	
                    preSchool.getMajors().add(major);
		                    
                    
            }
            schoolList.add(preSchool);
        } catch (Exception e) {   
        	  
            e.printStackTrace();   
  
        } finally {   
  
            readwb.close();   
  
        }  
		
		return schoolList;
	}
	
	public static List<School> getAllSchoolAndMajor(){


		List<School> schoolList = new ArrayList<School>();
		
		jxl.Workbook readwb = null;   
		
		List<String> provinceList = getAllProvince();
        try    
  
        {   
  
            //构建Workbook对象, 只读Workbook对象   
  
            //直接从本地文件创建Workbook   
  
            InputStream instream = new FileInputStream("211学校以及专业");   
  
            readwb = Workbook.getWorkbook(instream);   
  
    
  
            //Sheet的下标是从0开始   
  
            //获取第一张Sheet表   
  
            Sheet readsheet = readwb.getSheet(0);   
  
            //获取Sheet表中所包含的总列数   
  
            int rsColumns = readsheet.getColumns();   
  
            //获取Sheet表中所包含的总行数   
  
            int rsRows = readsheet.getRows();   
  
            //获取指定单元格的对象引用   
  
            String  preSchoolName =  readsheet.getCell(1, 1).getContents();
            School preSchool = new School();
            preSchool.setSchoolName(preSchoolName);
            
            for (int i = 1; i < rsRows; i++)   
            {   
     
  
                    Cell cell = readsheet.getCell(1, i);   
                    String schoolName = cell.getContents();
                    cell = readsheet.getCell(2, i);
                    String majorName = cell.getContents();
                    
                    if(!preSchool.getSchoolName().equals(schoolName)){
                    	
                    	schoolList.add(preSchool);
                    	preSchool = new School();
                    	preSchool.setSchoolName(schoolName);
                    	
                    }
                    for(int year = 2006; year < 2015; year ++){
                    	for(String provinceName :provinceList){
		                    Major major = new Major();
		                	major.setSpecialtyname(majorName);
		                	major.setYear(year + "");
		                	major.setLocalProvince(provinceName);
		                	major.setVar("0");
		                	major.setVar_score("0");
		                	major.setStudentType("理科");
		                	
		                	Major major1 = new Major();
		                	major1.setSpecialtyname(majorName);
		                	major1.setYear(year + "");
		                	major1.setLocalProvince(provinceName);
		                	major1.setVar("0");
		                	major1.setVar_score("0");
		                	major1.setStudentType("文科");
		                    preSchool.getMajorList().add(major);
		                    preSchool.getMajorList().add(major1);
                    	}
                    }
  
            }
            schoolList.add(preSchool);
        } catch (Exception e) {   
        	  
            e.printStackTrace();   
  
        } finally {   
  
            readwb.close();   
  
        }  
		
		return schoolList;
	}
	
	public static List<School> getSchoolList(){
		
		List<School> schoolList = new ArrayList<School>();
		
		jxl.Workbook readwb = null;   
		  
        try    
  
        {   
  
            //构建Workbook对象, 只读Workbook对象   
  
            //直接从本地文件创建Workbook   
  
            InputStream instream = new FileInputStream("211学校以及专业");   
  
            readwb = Workbook.getWorkbook(instream);   
  
    
  
            //Sheet的下标是从0开始   
  
            //获取第一张Sheet表   
  
            Sheet readsheet = readwb.getSheet(0);   
  
            //获取Sheet表中所包含的总列数   
  
            int rsColumns = readsheet.getColumns();   
  
            //获取Sheet表中所包含的总行数   
  
            int rsRows = readsheet.getRows();   
  
            //获取指定单元格的对象引用   
  
            for (int i = 1; i < rsRows; i++)   
  
            {   
                for (int j = 0; j < rsColumns; j++)   
  
                {   
  
                    Cell cell = readsheet.getCell(j, i);   
  
                    School school = new School();
                    school.setSchoolName(cell.getContents());
                    schoolList.add(school);
                }   
  
            }   
        } catch (Exception e) {   
        	  
            e.printStackTrace();   
  
        } finally {   
  
            readwb.close();   
  
        }  
		
		return schoolList;
	}
public static void saveAsEXCEL(School school,int index,int i){
		

        try    
        {
        	
        	WritableWorkbook book  =  Workbook.createWorkbook( new  File("school/" +  school.getSchoolName() + index +".xls " ));
            //  生成名为“第一页”的工作表，参数0表示这是第一页
           WritableSheet sheet  =  book.createSheet( " 第一页 " ,  0 );
            //  在Label对象的构造子中指名单元格位置是第一列第一行(0,0)
            //  以及单元格内容为test
           int rowNumber = 1;
           
        	   System.out.println("major size" + school.getMajorList().size());
        	   List<Major> majorList = school.getMajorList();
        	   
        	   for(; i<majorList.size();i++){
        		   
        		   Major major = majorList.get(i);
	        	   Label label  =   new  Label( 1,rowNumber,  school.getSchoolName());
	        	   
	        	   if(major!=null){
	        		   sheet.addCell(label);
		        	   Label label2  =   new  Label(2,rowNumber,   major.getSpecialtyname());
		        	   Label label3  =   new  Label(3,rowNumber,   major.getLocalProvince());
		        	   Label label4  =   new  Label(4,rowNumber,   major.getStudentType());
		        	   Label label5  =   new  Label(5,rowNumber,   major.getYear());
		        	   Label label6  =   new  Label(6,rowNumber,   major.getVar());
		        	   Label label7  =   new  Label(7,rowNumber,   major.getVar_score());
		        	  sheet.addCell(label2);
		              sheet.addCell(label3);
		              sheet.addCell(label4);
		              sheet.addCell(label5);
		              sheet.addCell(label6);
		              sheet.addCell(label7);
		               //  将定义好的单元格添加到工作表中
		              
		              
		               /**/ /*
		               * 生成一个保存数字的单元格 必须使用Number的完整包路径，否则有语法歧义 单元格位置是第二列，第一行，值为789.123
		                */
		              jxl.write.Number number  =   new  jxl.write.Number(0, rowNumber , rowNumber );
		              sheet.addCell(number);
		              rowNumber ++;
	        	   }

	        	   if(rowNumber>=60000)
	        		   break;
        	   }
           
            //  写入数据并关闭文件
           book.write();
           book.close();
           if(i<majorList.size()){
        	   saveAsEXCEL(school,index+1,i);
           }
        } catch (Exception e) {   
  
            e.printStackTrace();   
  
        }  
        
	}
	public static void saveAsEXCEL(List<School> list,int index){
		

        try    
        {
        	
        	WritableWorkbook book  =  Workbook.createWorkbook( new  File( " test" + index + ".xls " ));
            //  生成名为“第一页”的工作表，参数0表示这是第一页
           WritableSheet sheet  =  book.createSheet( " 第一页 " ,  0 );
            //  在Label对象的构造子中指名单元格位置是第一列第一行(0,0)
            //  以及单元格内容为test
           int rowNumber = 1;
           
           for(School school : list){
        	   System.out.println("major size" + school.getMajorList().size());   
        	   for(Major major : school.getMajorList()){
        		   
	        	   Label label  =   new  Label( 1,rowNumber,  school.getSchoolName());
	        	   Label label2  =   new  Label(2,rowNumber,   major.getSpecialtyname());
	        	   Label label3  =   new  Label(3,rowNumber,   major.getLocalProvince());
	        	   Label label4  =   new  Label(4,rowNumber,   major.getYear());
	        	   Label label5  =   new  Label(5,rowNumber,   major.getVar());
	        	   Label label6  =   new  Label(6,rowNumber,   major.getVar_score());
	               //  将定义好的单元格添加到工作表中
	              sheet.addCell(label);
	              sheet.addCell(label2);
	              sheet.addCell(label3);
	              sheet.addCell(label4);
	              sheet.addCell(label5);
	              sheet.addCell(label6);
	               /**/ /*
	               * 生成一个保存数字的单元格 必须使用Number的完整包路径，否则有语法歧义 单元格位置是第二列，第一行，值为789.123
	                */
	              jxl.write.Number number  =   new  jxl.write.Number(0, rowNumber , rowNumber );
	              sheet.addCell(number);
	              rowNumber ++;
        	   }
           }
           
            //  写入数据并关闭文件
           book.write();
           book.close();
  
        } catch (Exception e) {   
  
            e.printStackTrace();   
  
        }  
	}
   
  
}  