# Python 开发约束

## 技术栈
- **Web 框架**：`FastAPI`（轻量、性能好、内置依赖注入和数据校验）
- **ORM**：`SQLAlchemy`（功能强大，支持多种数据库）
- **数据校验**：`Pydantic`（FastAPI 内置，简
- **包管理**：`UV`（比 pip 更快更安全）
- **数据库迁移**：`Alembic`
- **测试框架**：`pytest` + `pytest-mock`
- **依赖注入**：`FastAPI` 的 `Depends`
- **格式化工具**：`black`
- **日志**：`loguru`

## 一、核心思路：用 Python 实现 Spring 的分层架构

Spring 的核心规范是**严格的分层**：
```
Controller（接收请求） → Service（业务逻辑） → Repository（数据访问）
```

Python 也可以完全照搬这个模式，关键是**用约定和工具强制分离**。

### 1. 项目结构规范（最重要）

**错误示范（屎山温床）**：
```
app.py  # 路由、数据库查询、业务逻辑全挤在一起，几千行
```

**规范示范（仿 Spring Boot 结构）**：
```
myproject/
├── app.py                 # 应用入口（类似 SpringBootApplication）
├── config.py              # 配置文件
├── controllers/           # 控制器层（只负责参数校验、响应格式）
│   ├── user_controller.py
│   └── order_controller.py
├── services/              # 业务逻辑层（核心逻辑，可复用）
│   ├── user_service.py
│   └── order_service.py
├── repositories/          # 数据访问层（只做数据库操作）
│   ├── user_repo.py
│   └── order_repo.py
├── models/                # 数据模型/实体（类似 JPA Entity）
│   ├── user.py
│   └── order.py
├── schemas/               # 请求/响应数据结构（类似 Spring 的 DTO）
│   ├── user_schema.py
│   └── order_schema.py
├── middleware/            # 中间件（日志、鉴权、异常处理）
├── utils/                 # 工具类
└── tests/                 # 单元测试
```

### 2. 具体实现技术栈选择

| Spring 功能 | Python 替代方案 | 说明 |
|------------|----------------|------|
| 依赖注入（IoC） | `dependency-injector` 或 `FastAPI` 的 `Depends` | 强烈推荐后者，轻量且强制 |
| 分层架构强制 | 无框架强制，靠 **代码审查 + 目录结构约定** | 需要团队纪律 |
| ORM（数据访问） | `SQLAlchemy`（比 JPA 更强大）或 `Tortoise-ORM` | 用 Repository 模式封装 |
| 参数校验 + DTO | `Pydantic`（FastAPI 内置） | 比 Spring 的 Bean Validation 更简洁 |
| 接口规范（REST） | `FastAPI`（自动生成 Swagger 文档） | 比 Spring 的 Swagger 配置更简单 |
| 数据库迁移 | `Alembic` | 类似 Flyway/Liquibase |
| 单元测试 | `pytest` + `pytest-mock` | 比 JUnit 更简洁 |
| 事务管理 | `SQLAlchemy` 的 `session` 或装饰器 | 不如 Spring `@Transactional` 优雅，但能实现 |

### 3. 关键实战示例（用 FastAPI + SQLAlchemy 实现规范分层）

#### **模型层（models/user.py）** - 类似 JPA Entity
```python
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), nullable=False)
```

#### **DTO/Schema 层（schemas/user_schema.py）** - 类似 Spring 的 DTO
```python
from pydantic import BaseModel, EmailStr

class UserCreateRequest(BaseModel):  # 请求体
    username: str
    email: EmailStr

class UserResponse(BaseModel):       # 响应体
    id: int
    username: str
    email: str
```

#### **Repository 层（repositories/user_repo.py）** - 只做数据库操作
```python
from sqlalchemy.orm import Session
from models.user import User

class UserRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, user_data: dict) -> User:
        user = User(**user_data)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def find_by_username(self, username: str) -> User | None:
        return self.db.query(User).filter(User.username == username).first()
```

#### **Service 层（services/user_service.py）** - 业务逻辑
```python
from repositories.user_repo import UserRepository
from schemas.user_schema import UserCreateRequest

class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo
    
    def register_user(self, request: UserCreateRequest) -> dict:
        # 业务逻辑：检查用户名是否已存在
        existing = self.repo.find_by_username(request.username)
        if existing:
            raise ValueError("Username already exists")
        
        # 可以加密码加密、发送邮件等业务逻辑
        user = self.repo.create(request.dict())
        return {"id": user.id, "username": user.username}
```

#### **Controller 层（controllers/user_controller.py）** - 只处理 HTTP
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from services.user_service import UserService
from repositories.user_repo import UserRepository
from schemas.user_schema import UserCreateRequest, UserResponse
from database import get_db  # 依赖注入数据库会话

router = APIRouter(prefix="/users", tags=["users"])

# 依赖注入链：db → repo → service
def get_user_service(db: Session = Depends(get_db)):
    repo = UserRepository(db)
    return UserService(repo)

@router.post("/register", response_model=UserResponse)
def register(request: UserCreateRequest, service: UserService = Depends(get_user_service)):
    try:
        return service.register_user(request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
```

#### **入口（app.py）** - 类似 SpringBootApplication
```python
from fastapi import FastAPI
from controllers import user_controller

app = FastAPI(title="My规范项目")
app.include_router(user_controller.router)
```

## 二、Python 保持规范的关键技巧

### 1. **强制依赖注入（不要 new）**
- ❌ 坏习惯：`service = UserService()` 在 Controller 里直接 new
- ✅ 好习惯：通过 `Depends` 或依赖注入容器，让调用链清晰

### 2. **使用类型注解 + 静态检查**
```bash
pip install mypy pylint
```
类型注解能防止 Spring 开发者最反感的 Python 问题：运行时才发现传错类型。

### 3. **数据库事务边界明确**
Spring 的 `@Transactional` 很方便。Python 中用上下文管理器模拟：
```python
class UserService:
    def transfer_money(self, from_id, to_id, amount):
        with self.db.begin():  # 显式事务边界
            # 多个数据库操作...
            pass
```

### 4. **编写单元测试强制解耦**
如果代码写得不规范（比如 Service 里直接操作数据库），就很难 mock。规范的代码一定能轻松测试：
```python
def test_register_user(mocker):
    mock_repo = mocker.Mock()
    mock_repo.find_by_username.return_value = None  # 用户名不存在
    service = UserService(mock_repo)
    
    result = service.register_user(UserCreateRequest(username="test", email="a@b.com"))
    assert result["username"] == "test"
    mock_repo.create.assert_called_once()
```

## 三、常见陷阱与解决办法

| 问题 | 后果 | 解决办法 |
|------|------|----------|
| Service 层直接使用 `request` 对象 | 难以复用和测试 | Service 接收简单类型或 DTO |
| 全局数据库连接 | 无法切换数据源、难以测试 | 通过依赖注入传递 Session |
| 没有统一的异常处理 | 错误响应格式混乱 | 全局 `@app.exception_handler` |
| 循环依赖（A service 依赖 B，B 依赖 A） | 代码混乱 | 重新设计职责，或使用依赖注入容器延迟解析 |

