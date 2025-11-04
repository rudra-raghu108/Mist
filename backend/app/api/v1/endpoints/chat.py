diff --git a/app/api/v1/endpoints/chat.py b/app/api/v1/endpoints/chat.py
index a3fea7a68a20e3748ea5dccf9a3dea06a9a19be7..daeb3aaff04d7c534028150dfab335c397c95ff1 100644
--- a/app/api/v1/endpoints/chat.py
+++ b/app/api/v1/endpoints/chat.py
@@ -178,120 +178,120 @@ async def send_message(
             chat_id=chat_id,
             user_id=current_user.id
         )
         db.add(user_message)
         db.commit()
         db.refresh(user_message)
         
         # Get chat history for context
         chat_history = db.query(Message).filter(
             Message.chat_id == chat_id
         ).order_by(Message.created_at.desc()).limit(10).all()
         
         # Generate AI response
         ai_response_data = await ai_service.generate_response(
             user_message=message_data.content,
             user=current_user,
             chat_history=chat_history
         )
         
         # Save AI response
         ai_message = Message(
             content=ai_response_data["content"],
             role=MessageRole.ASSISTANT,
             chat_id=chat_id,
             user_id=None,  # AI message
-            metadata={
+            extra_metadata={
                 "tokens_used": ai_response_data["tokens_used"],
                 "model_used": ai_response_data["model_used"],
-                "category": ai_response_data["category"]
-            }
+                "category": ai_response_data["category"],
+            },
         )
         db.add(ai_message)
         
         # Update chat title if it's the first message
         if not chat.title:
             chat.title = message_data.content[:50] + "..." if len(message_data.content) > 50 else message_data.content
         
         chat.updated_at = datetime.utcnow()
         db.commit()
         db.refresh(ai_message)
         
         return MessageResponse(
             id=ai_message.id,
             content=ai_message.content,
             role=ai_message.role,
             chat_id=ai_message.chat_id,
             user_id=ai_message.user_id,
-            metadata=ai_message.metadata,
+            metadata=ai_message.extra_metadata,
             created_at=ai_message.created_at
         )
         
     except Exception as e:
         raise HTTPException(
             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
             detail=f"Failed to send message: {str(e)}"
         )
 
 
 @router.get("/chats/{chat_id}/messages", response_model=List[MessageResponse])
 async def get_chat_messages(
     chat_id: str,
     limit: int = 50,
     offset: int = 0,
     current_user: User = Depends(auth_service.get_current_user),
     db: Session = Depends(get_db)
 ):
     """Get messages for a specific chat"""
     try:
         # Verify chat exists and belongs to user
         chat = db.query(Chat).filter(
             Chat.id == chat_id,
             Chat.user_id == current_user.id
         ).first()
         
         if not chat:
             raise HTTPException(
                 status_code=status.HTTP_404_NOT_FOUND,
                 detail="Chat not found"
             )
         
         messages = db.query(Message).filter(
             Message.chat_id == chat_id
         ).order_by(Message.created_at.desc()).offset(offset).limit(limit).all()
         
         # Reverse to get chronological order
         messages.reverse()
         
         return [
             MessageResponse(
                 id=message.id,
                 content=message.content,
                 role=message.role,
                 chat_id=message.chat_id,
                 user_id=message.user_id,
-                metadata=message.metadata,
+                metadata=message.extra_metadata,
                 created_at=message.created_at
             ) for message in messages
         ]
         
     except Exception as e:
         raise HTTPException(
             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
             detail=f"Failed to get messages: {str(e)}"
         )
 
 
 @router.get("/suggestions")
 async def get_quick_suggestions(
     current_user: User = Depends(auth_service.get_current_user)
 ):
     """Get quick suggestion buttons for the user"""
     try:
         suggestions = await ai_service.generate_quick_suggestions(current_user)
         return {"suggestions": suggestions}
         
     except Exception as e:
         raise HTTPException(
             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
             detail=f"Failed to get suggestions: {str(e)}"
         )
