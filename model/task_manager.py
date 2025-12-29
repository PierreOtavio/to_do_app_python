from model.engine import Session, Storage
from controller.new_task import NewTask

class TaskManager:
    
    def __init__(self, session) -> None:
        self.session = session

    @staticmethod
    def list_task(session, status = None) -> list:
        query = session.query(Storage)

        if status == False:
            query = query.filter(Storage.complete == False)
        elif status == True:
            query = query.filter(Storage.complete == True)

        query.order_by(Storage.complete, Storage.created_at.desc()).first()

        try:
            return query.all()
        except Exception as e:
            print(f"{e}")
            return []
        
    @staticmethod
    def exclude_task(id: int, session) -> bool:
        query = session.query(Storage).filter(Storage.id == id).first()
        try:
            if query:
                session.delete(query)
                session.commit()
                return True
            else:
                print("Tarefa não realizada, ID não encontrado")
                return False
        except Exception as e:
            print(f"Unexpected failure: {e}")
            session.rollback()
            return False

    @staticmethod
    def update_task(session, id:int, **kwargs) -> bool:

        task = session.query(Storage).filter(Storage.id == id).first()

        if not task:
            print("ID não encontrado")
            return False
        
        for key, value in kwargs.items():
            if hasattr(task, key):
                setattr(task, key, value)
            else:
                print(f"O campo {key} não é um atributo válido")

        try:
            session.commit()
            return True
        except Exception as e:
            print(f"{e}")
            session.rollback()
            return False
        
    @staticmethod
    def add_task(session, task_data: NewTask) -> Storage | None:

        description = task_data.description.strip()

        if not description:
            return None
        
        final_ = description[:100]

        new_task = Storage(
            task = final_,
            description = description,
            complete = task_data.complete
        )

        try:
            session.add(new_task)
            session.commit()
            return new_task
        except Exception as e:
            print(f"{e}")
            session.rollback()
            return None
    
    @staticmethod
    def filter_task(session, filters: dict):

        if filters is None:
            return []
        
        try:
            ss_query = session.query(Storage)
            status = filters.get("complete")

            if status is not None:
                    ss_query = ss_query.filter(Storage.complete == status)
            if filters.get("task"):
                ss_query = ss_query.filter(Storage.task.like(f"%{filters['task']}%"))
            if filters.get("description"):
                ss_query = ss_query.filter(Storage.description.like(f"%{filters['description']}%"))
            if filters.get("id"):
                ss_query = ss_query.filter(Storage.id == filters["id"])
            
            print(ss_query)
            lst_final = ss_query.order_by(Storage.complete, Storage.created_at.desc()).all()

            return lst_final
        except Exception as e:  
            print(f"Errors: {e}")
            return []