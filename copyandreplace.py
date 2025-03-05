import bpy

# الحصول على جميع الأجسام المحددة
selected_objects = bpy.context.selected_objects

# الجسم النشط هو المصدر
source_obj = bpy.context.object

# التحقق من أن هناك أجسام محددة وأن الجسم النشط موجود
if not source_obj or len(selected_objects) < 2:
    print("يجب تحديد جسم واحد على الأقل ليتم استبداله بالإضافة إلى الجسم المصدر!")
else:
    # الأجسام التي سيتم استبدالها هي كل الأجسام المحددة ما عدا الجسم النشط (المصدر)
    target_objects = [obj for obj in selected_objects if obj != source_obj]

    for target_obj in target_objects:
        # إنشاء نسخة جديدة من المصدر
        new_obj = source_obj.copy()
        new_obj.data = source_obj.data.copy()
        bpy.context.collection.objects.link(new_obj)
        
        # جعل النسخة الجديدة تأخذ نفس الموقع والدوران تمامًا كالجسم القديم
        new_obj.matrix_world = target_obj.matrix_world.copy()
        
        # إذا كان الهدف لديه Action، ربطه بالنسخة الجديدة
        if target_obj.animation_data and target_obj.animation_data.action:
            new_obj.animation_data_create()
            new_obj.animation_data.action = target_obj.animation_data.action
        
        # حذف الجسم القديم
        bpy.data.objects.remove(target_obj)

    print(f"تم استبدال {len(target_objects)} أجسام بالجسم '{source_obj.name}'.")

