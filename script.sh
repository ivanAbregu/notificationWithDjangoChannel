
docker exec -ti backend-notification bash -c '

echo "from main.consumers import *
from django.contrib.auth import get_user_model
User = get_user_model()
user = User.objects.first()
send_notification_to_customer(user.id, f\"aca vaa la notification for user id: {user.id} \")
" | ./manage.py shell || exit 1
'