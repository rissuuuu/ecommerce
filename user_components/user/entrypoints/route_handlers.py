import json
from lib.json_encoder import jsonable_encoder

from sanic.views import HTTPMethodView
from user_components.user.views import views

from entrypoint.messagebus import messagebus
from lib import err_msg
from pydantic import ValidationError
from sanic import response
from user_components.user.adapters import repository
from user_components.user.domain import command, exceptions
from user_components.user.service_layer import abstract, unit_of_work
from user_components.user.utils.decorator import authorized
from user_components.user.service_layer import query


async def user_register(request):
    try:
        user_data = abstract.AddUser(**request.json)
        otp_res = await messagebus.handle(
            message=command.AddUser(**user_data.dict()),
            uow=unit_of_work.UserSQLAlchemyUnitofWork(
                connection=request.app.ctx.db,
                repository_class=repository.UserSqlRepository,
            ),
        )
        for otp in otp_res:
            my_otp = otp
    except exceptions.InvalidPhoneNumber:
        return response.json({"error": err_msg.PHONE_NUMBER_INVALID}, status=400)
    except ValidationError as e:
        return response.json(json.loads(e.json()), status=400)
    except exceptions.UserExists:
        return response.json({"error": "User already exists"}, status=400)

    return response.json({"OTP": my_otp}, status=201)


async def user_activate(request):
    try:
        activate_user = abstract.ActivateUser(**request.json)
        await messagebus.handle(
            message=command.ActivateUser(**activate_user.dict()),
            uow=unit_of_work.UserSQLAlchemyUnitofWork(
                connection=request.app.ctx.db,
                repository_class=repository.UserSqlRepository,
            ),
        )
    except exceptions.OTP_NOT_FOUND:
        return response.json({"error": err_msg.OTP_NOT_FOUND})
    except exceptions.OTP_MISMATCHED:
        return response.json({"error": err_msg.OTP_MISMATCHED})
    return response.json({"success": "User Activated Successfully. Please Login"})


async def user_login(request):
    try:
        user = abstract.LoginUser(**request.json)
        login_result = await messagebus.handle(
            message=command.LoginUser(**user.dict()),
            uow=unit_of_work.UserSQLAlchemyUnitofWork(
                connection=request.app.ctx.db,
                repository_class=repository.UserSqlRepository,
            ),
        )
        result = login_result.pop(0)
        request.ctx.session[result["user"]["id"]] = result["user"]
        return response.json({"token": result["token"]})
    except exceptions.INVALID_EMAIL_PASSWORD:
        return response.json({"error": err_msg.INVALID_EMAIL_PASSWORD}, status=400)
    except exceptions.USER_DOES_NOT_EXIST:
        return response.json({"error": err_msg.USER_DOES_NOT_EXIST}, status=400)
    except exceptions.USER_NOT_ACTIVE:
        return response.json({"error": err_msg.USER_NOT_ACTIVE}, status=400)
    except exceptions.PASSWORD_INCORRECT:
        return response.json({"error": err_msg.PASSWORD_INCORRECT}, status=400)


@authorized()
async def change_password(request):
    try:
        change_password = abstract.ChangePassword(**request.json)
        await messagebus.handle(
            message=command.ChangePassword(**change_password.dict()),
            uow=unit_of_work.UserSQLAlchemyUnitofWork(
                connection=request.app.ctx.db,
                repository_class=repository.UserSqlRepository,
            ),
        )
    except exceptions.USER_DOES_NOT_EXIST:
        return response.json({"error": err_msg.USER_DOES_NOT_EXIST})
    except exceptions.PASSWORD_INCORRECT:
        return response.json({"error": err_msg.PASSWORD_INCORRECT})
    except ValidationError as e:
        return response.json(json.loads(e.json()), status=400)
    return response.json({"success": "password changed successfully"})


async def forgot_password(request):
    try:
        forget_password = abstract.ForgetPassword(**request.json)
        otp_res = await messagebus.handle(
            message=command.ForgetPassword(**forget_password.dict()),
            uow=unit_of_work.UserSQLAlchemyUnitofWork(
                connection=request.app.ctx.db,
                repository_class=repository.UserSqlRepository,
            ),
        )
        for otp in otp_res:
            my_otp = otp
    except exceptions.REDIS_CONNECTION_NOT_ESTABLISHED:
        return response.text(err_msg.REDIS_CONNECTION_NOT_ESTABLISHED)

    except exceptions.USER_DOES_NOT_EXIST:
        return response.json({"error": err_msg.USER_DOES_NOT_EXIST}, status=400)

    except ValidationError as e:
        return response.json(json.loads(e.json()), status=400)
    return response.json({"OTP": my_otp})


async def forget_password_update(request):
    try:
        forget_password = abstract.ForgetPasswordUpdate(**request.json)
        await messagebus.handle(
            message=command.ForgetPasswordUpdate(**forget_password.dict()),
            uow=unit_of_work.UserSQLAlchemyUnitofWork(
                connection=request.app.ctx.db,
                repository_class=repository.UserSqlRepository,
            ),
        )
    except exceptions.REDIS_CONNECTION_NOT_ESTABLISHED:
        return response.json(
            {"error": err_msg.REDIS_CONNECTION_NOT_ESTABLISHED}, status=400
        )
    except exceptions.USER_DOES_NOT_EXIST:
        return response.json({"error": err_msg.USER_DOES_NOT_EXIST}, status=400)
    except exceptions.OTP_NOT_FOUND:
        return response.json({"error": err_msg.OTP_NOT_FOUND}, status=400)
    except exceptions.OTP_MISMATCHED:
        return response.json({"error": err_msg.OTP_MISMATCHED}, status=400)
    except ValidationError as e:
        return response.json(json.loads(e.json()), status=400)
    return response.json({"success": "password changed successfully"})


async def resend_otp(request):
    resend_otp = abstract.ResendOtp(**request.json)
    try:
        await messagebus.handle(
            message=command.ResendOtp(**resend_otp.dict()),
            uow=unit_of_work.UserSQLAlchemyUnitofWork(
                connection=request.app.ctx.db,
                repository_class=repository.UserSqlRepository,
            ),
        )
        return response.text("OTP Resent")
    except exceptions.DATA_NOT_FOUND:
        return response.text(err_msg.DATA_NOT_FOUND)


class UserRoutes(HTTPMethodView):
    async def get(self, request, user_id):
        page = request.args.get("page")
        q_model = query.UserQueryParamModel(page=page)

        if user_id:
            q_model.id_ = user_id
            user_res = await views.get_user_by_uuid(q_model.id_, request.app.ctx.db)
            # return response.json(jsonable_encoder(user))
            res = [jsonable_encoder(user_res)]
        else:
            user_res = await views.get_users(request.app.ctx.db, page=q_model.page)
            res = jsonable_encoder(user_res)
        user = []
        for item in res:
            item.pop("created_at")
            item.pop("password")
            item.pop("updated_at")
            user.append(item)

        return response.json(user)
