"""
Service for Trello analytics and reporting.
"""

from typing import Dict, Any, List
from datetime import datetime
from collections import defaultdict
from server.utils.trello_api import TrelloClient


class AnalyticsService:
    """Service for analytics and reporting operations."""

    def __init__(self, client: TrelloClient):
        """
        Initialize the analytics service.

        Args:
            client: Trello API client instance
        """
        self.client = client

    def get_board_statistics(self, board_id: str) -> Dict[str, Any]:
        """
        Get comprehensive statistics for a board.

        Args:
            board_id: The ID of the board

        Returns:
            Dictionary containing board statistics
        """
        # Get board with all data
        params = {
            "cards": "all",
            "lists": "all",
            "members": "all",
            "labels": "all",
            "actions": "all",
            "actions_limit": "1000"
        }
        board = self.client.get(f"/boards/{board_id}", params=params)
        
        # Calculate statistics
        stats = {
            "board_name": board.get("name"),
            "board_id": board_id,
            "total_lists": len(board.get("lists", [])),
            "total_cards": len(board.get("cards", [])),
            "total_members": len(board.get("members", [])),
            "total_labels": len(board.get("labels", [])),
            "open_cards": len([c for c in board.get("cards", []) if not c.get("closed")]),
            "closed_cards": len([c for c in board.get("cards", []) if c.get("closed")]),
            "cards_with_due_dates": len([c for c in board.get("cards", []) if c.get("due")]),
            "overdue_cards": len([c for c in board.get("cards", []) if c.get("due") and not c.get("dueComplete") and datetime.fromisoformat(c.get("due").replace("Z", "+00:00")) < datetime.now(datetime.now().astimezone().tzinfo)]),
            "completed_cards": len([c for c in board.get("cards", []) if c.get("dueComplete")]),
        }
        
        # Cards per list
        cards_per_list = defaultdict(int)
        for card in board.get("cards", []):
            if not card.get("closed"):
                list_id = card.get("idList")
                cards_per_list[list_id] += 1
        
        # Find list names
        list_names = {lst["id"]: lst["name"] for lst in board.get("lists", [])}
        stats["cards_per_list"] = {
            list_names.get(lid, lid): count 
            for lid, count in cards_per_list.items()
        }
        
        # Label usage
        label_usage = defaultdict(int)
        for card in board.get("cards", []):
            for label_id in card.get("idLabels", []):
                label_usage[label_id] += 1
        
        label_names = {lbl["id"]: lbl["name"] or lbl["color"] for lbl in board.get("labels", [])}
        stats["label_usage"] = {
            label_names.get(lid, lid): count 
            for lid, count in label_usage.items()
        }
        
        # Member activity
        member_actions = defaultdict(int)
        for action in board.get("actions", []):
            member_id = action.get("idMemberCreator")
            if member_id:
                member_actions[member_id] += 1
        
        member_names = {mbr["id"]: mbr.get("fullName", mbr.get("username")) for mbr in board.get("members", [])}
        stats["member_activity"] = {
            member_names.get(mid, mid): count 
            for mid, count in member_actions.items()
        }
        
        return stats

    def get_card_cycle_time(self, board_id: str) -> Dict[str, Any]:
        """
        Calculate average time cards spend in each list.

        Args:
            board_id: The ID of the board

        Returns:
            Dictionary containing cycle time statistics
        """
        # Get board actions
        params = {
            "filter": "updateCard:idList",
            "limit": "1000"
        }
        actions = self.client.get(f"/boards/{board_id}/actions", params=params)
        
        # Get lists
        lists = self.client.get(f"/boards/{board_id}/lists")
        list_names = {lst["id"]: lst["name"] for lst in lists}
        
        # Calculate time in each list
        card_times = defaultdict(lambda: defaultdict(list))
        card_current_list = {}
        card_list_enter_time = {}
        
        # Process actions in reverse chronological order
        for action in reversed(actions):
            card_id = action.get("data", {}).get("card", {}).get("id")
            list_after = action.get("data", {}).get("listAfter", {}).get("id")
            list_before = action.get("data", {}).get("listBefore", {}).get("id")
            action_date = action.get("date")
            
            if card_id and list_after:
                # Card moved to new list
                if card_id in card_current_list and card_id in card_list_enter_time:
                    # Calculate time in previous list
                    prev_list = card_current_list[card_id]
                    enter_time = datetime.fromisoformat(card_list_enter_time[card_id].replace("Z", "+00:00"))
                    exit_time = datetime.fromisoformat(action_date.replace("Z", "+00:00"))
                    duration = (exit_time - enter_time).total_seconds() / 3600  # hours
                    card_times[prev_list]["durations"].append(duration)
                
                card_current_list[card_id] = list_after
                card_list_enter_time[card_id] = action_date
        
        # Calculate averages
        cycle_times = {}
        for list_id, data in card_times.items():
            durations = data["durations"]
            if durations:
                cycle_times[list_names.get(list_id, list_id)] = {
                    "average_hours": sum(durations) / len(durations),
                    "min_hours": min(durations),
                    "max_hours": max(durations),
                    "card_count": len(durations)
                }
        
        return {
            "board_id": board_id,
            "cycle_times": cycle_times
        }
