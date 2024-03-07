from flask import Flask, jsonify, request
from utilities.utilities import*
from configuration.config import db
cursor=db.cursor()
def selectcourseId(as_id):
    try:
        cursor.execute('SELECT course_id FROM tb_assessment WHERE as_id = %s', (as_id,))
        result = cursor.fetchone()
        if result is not None:
            return result[0]
        else:
            return None  # or raise an exception or set a default value
    except Exception as e:
    # Log the exception
        print(f"Error: {e}")

def checkAssessmentCompletion(student_id,as_id):
    try:
        # Fetch the total assessment number required for the course
        course_id = selectcourseId(as_id)
        # if course_id is None:
        #     return jsonify({'message': 'Student is not enrolled in any courses.'})
        # else:
        cursor.execute('SELECT COUNT(*) as count FROM tb_attendance ad JOIN tb_assessment at ON ad.assessment_id = at.as_id WHERE ad.student_id = %s AND at.course_id = %s', (student_id, course_id))
        completed_assessments_count = cursor.fetchone()[0]
        return completed_assessments_count,course_id
    except Exception as e:
        return jsonify({'error': str(e)})
def checkTotalAssessment(course_id):
    try:
        cursor.execute('SELECT assessment_no FROM tb_course WHERE course_id = %s',(course_id,))
        total_assessment=cursor.fetchone()[0]
        return total_assessment
        #return jsonify(total_assessment)
    except Exception as e:
        return jsonify({'Error':str(e)})

def checkBadge(student_id,assessment_id,attendance_score):
    cursor.execute('SELECT * FROM tb_attendance WHERE student_id = %s AND assessment_id = %s', (student_id, assessment_id))
    existing_record = cursor.fetchone()
    if existing_record:
        # If the record already exists, you may choose to skip the insertion or update the existing record
        return {'message': 'Attendance score already exists for this student and assessment'}
    else:
        if int(attendance_score) >= 8:
            badge=1
            # If the record doesn't exist, execute an SQL query to insert the new data
            cursor.execute('INSERT INTO tb_attendance (badge,attendance_score, student_id, assessment_id) VALUES (%s, %s, %s, %s)',(badge, attendance_score,student_id, assessment_id))
            db.commit()
            coins=addBadgeacoin(student_id,assessment_id)
            return {"badge":1,"coins":coins}
        else:
            cursor.execute('INSERT INTO tb_attendance (attendance_score, student_id, assessment_id) VALUES (%s, %s, %s)', (attendance_score,student_id, assessment_id))
            db.commit()
            return {"badge":0,"coins":0}
                
def addBadgeacoin(student_id,assessment_id):
    cursor.execute('select coins from tb_assessment where as_id=%s',(assessment_id,))
    supercoin=cursor.fetchone()[0]
    cursor.execute('select coins from tb_supercoin where student_id=%s',(student_id,))
    studentcoin=cursor.fetchone()[0]
    coins=supercoin+studentcoin
    cursor.execute('update tb_supercoin set coins=%s where student_id=%s',(coins,student_id))
    db.commit()
    return supercoin

def addcertifatecoin(student_id,course_id):
    cursor.execute('select coins from tb_course where course_id=%s',(course_id,))
    supercoin=cursor.fetchone()[0]
    cursor.execute('select coins from tb_supercoin where student_id=%s',(student_id,))
    studentcoin=cursor.fetchone()[0]
    coins=supercoin+studentcoin
    cursor.execute('update tb_supercoin set coins=%s where student_id=%s',(coins,student_id))
    db.commit()
    return supercoin

def certificate(student_id,assessment_id):
    course_id=selectcourseId(assessment_id)
    cursor.execute('SELECT COALESCE(SUM(aa.attendance_score), 0) as total_score FROM tb_attendance aa JOIN tb_assessment a ON aa.assessment_id = a.as_id WHERE aa.student_id = %s AND a.course_id = %s',(student_id,course_id))
    total_score=cursor.fetchone()[0]
    assessment_no=checkTotalAssessment(course_id)
    percentage =int(total_score/assessment_no)*10
    if int(percentage)>60:
        certificate=1
        status="completed"
        cursor.execute('UPDATE tb_enrollment SET certificate = %s,score=%s,status=%s WHERE student_id = %s AND course_id = %s',(certificate,total_score,status,student_id, course_id))                     
        db.commit()
        coins=addcertifatecoin(student_id,course_id)
        return {"certificate":1,"coins":coins} 
    else:
        certificate=0
        status="completed"
        update_certificate = 'UPDATE tb_enrollment SET certificate = %s,score=%s,status=%s WHERE student_id = %s AND course_id = %s' 
        cursor.execute(update_certificate,(certificate,total_score,status,student_id, course_id))                      
        db.commit()
        return {"certificate":0,"coins":0} 
def certification(student_id,assessment_id,score):
    course_id=selectcourseId(assessment_id)
    cursor.execute("select * from tb_enrollment where student_id=%s and course_id=%s",(student_id,course_id))
    check=cursor.fetchone()
    # if not check:
    #     return jsonify({'messege':"not entrolled to this course"})
    badge_result=checkBadge(student_id,assessment_id,score)
    completed_assessment,id=checkAssessmentCompletion(student_id,assessment_id)
    total_assessment=checkTotalAssessment(id)
    if total_assessment==completed_assessment:
        cert_result=certificate(student_id,assessment_id)
        return generate_response({"badge":badge_result,"certificate":cert_result})
    else:
        return generate_response({"badge":badge_result,"certificate":None})
